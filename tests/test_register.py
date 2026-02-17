from db.models import Users

def test_register_helpee_adds_user_to_database(client, app):
    resp = client.post(
        "/register_helpee",
        data={
            "first_name": "Rory",
            "last_name": "OGorman",
            "email": "rorytest123@gmail.com",
            "location": "Dundalk",
            "password": "Test1234567!",
            "confirm_password": "Test1234567!",
        },
        follow_redirects=False,  
    )

    assert resp.status_code == 302
    assert "/home_page/" in resp.headers["Location"]

   
    with app.app_context():
        user = Users.query.filter_by(email="rorytest123@gmail.com").first()
        assert user is not None
        assert user.name == "Rory OGorman"
        assert user.type == "helpee"
        assert user.work_area == "Dundalk"
