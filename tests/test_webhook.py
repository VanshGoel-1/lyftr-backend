import json
import os
from tests.conftest import sign

SECRET = os.environ["WEBHOOK_SECRET"]

BODY = {
    "message_id": "t1",
    "from": "+919876543210",
    "to": "+14155550100",
    "ts": "2025-01-15T10:00:00Z",
    "text": "Hello"
}

def test_invalid_signature(client):
    r = client.post(
        "/webhook",
        json=BODY,
        headers={"X-Signature": "bad"}
    )
    assert r.status_code == 401

def test_valid_signature(client):
    raw = json.dumps(BODY).encode()
    sig = sign(SECRET, raw)

    r = client.post(
        "/webhook",
        data=raw,
        headers={
            "Content-Type": "application/json",
            "X-Signature": sig
        }
    )

    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_duplicate_is_idempotent(client):
    raw = json.dumps(BODY).encode()
    sig = sign(SECRET, raw)

    r = client.post(
        "/webhook",
        data=raw,
        headers={
            "Content-Type": "application/json",
            "X-Signature": sig
        }
    )

    assert r.status_code == 200
