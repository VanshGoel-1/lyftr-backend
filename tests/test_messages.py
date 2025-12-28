def test_list_messages(client):
    r = client.get("/messages")
    assert r.status_code == 200
    body = r.json()

    assert "data" in body
    assert "total" in body
    assert body["total"] >= 1

def test_pagination(client):
    r = client.get("/messages?limit=1&offset=0")
    assert r.status_code == 200
    body = r.json()

    assert body["limit"] == 1
    assert body["offset"] == 0
    assert len(body["data"]) == 1
