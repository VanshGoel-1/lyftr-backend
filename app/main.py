import hmac, hashlib, time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from app.config import WEBHOOK_SECRET
from app.models import init_db
from app.schemas import WebhookMessage
from app.storage import insert_message, list_messages
from app.logging_utils import json_log
from app.metrics import HTTP_COUNTER, WEBHOOK_COUNTER, LATENCY, generate_latest

app = FastAPI()

@app.on_event("startup")
def startup():
    if not WEBHOOK_SECRET:
        raise RuntimeError("WEBHOOK_SECRET not set")
    init_db()

@app.get("/health/live")
def live():
    return {"status": "live"}

@app.get("/health/ready")
def ready():
    if not WEBHOOK_SECRET:
        raise HTTPException(503)
    return {"status": "ready"}

@app.post("/webhook")
async def webhook(req: Request):
    start = time.time()
    raw = await req.body()
    sig = req.headers.get("X-Signature")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw,
        hashlib.sha256
    ).hexdigest()

    if sig != expected:
        WEBHOOK_COUNTER.labels("invalid_signature").inc()
        raise HTTPException(401, detail="invalid signature")

    try:
        payload = WebhookMessage.parse_raw(raw)
    except Exception:
        WEBHOOK_COUNTER.labels("validation_error").inc()
        raise

    result = insert_message(payload.dict(by_alias=True))
    WEBHOOK_COUNTER.labels(result).inc()

    latency = (time.time() - start) * 1000
    LATENCY.observe(latency)

    json_log(
        level="INFO",
        method="POST",
        path="/webhook",
        status=200,
        latency_ms=int(latency),
        message_id=payload.message_id,
        dup=result == "duplicate",
        result=result
    )

    return {"status": "ok"}

@app.get("/messages")
def messages(limit: int = 50, offset: int = 0, from_: str = None, since: str = None, q: str = None):
    total, rows = list_messages(
        {"from": from_, "since": since, "q": q},
        limit, offset
    )
    return {
        "data": [
            {
                "message_id": r[0],
                "from": r[1],
                "to": r[2],
                "ts": r[3],
                "text": r[4]
            } for r in rows
        ],
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()
