import json, time, uuid, logging
from datetime import datetime

def json_log(**kwargs):
    base = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "request_id": str(uuid.uuid4()),
    }
    base.update(kwargs)
    print(json.dumps(base))
