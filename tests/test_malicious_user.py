def test_cannot_access_home_page_without_login(client):
    resp = client.get("/home_page/", follow_redirects=False)

    assert resp.status_code in (302, 303)
    assert resp.headers["Location"] == "/"