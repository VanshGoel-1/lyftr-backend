import os
import hmac
import hashlib
import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

def sign(secret: str, body: bytes) -> str:
    return hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
