def test_live(client):
    r = client.get("/health/live")
    assert r.status_code == 200

def test_ready(client):
    r = client.get("/health/ready")
    assert r.status_code == 200
