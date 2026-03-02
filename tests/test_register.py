from flask import url_for
from db.models import Users

def test_register_adds_user_to_database(client, app):
    with app.test_request_context():
        register_url = url_for("login.register")

    resp = client.post(
        register_url,
        data={
            "first_name": "Rory",
            "last_name": "OGorman",
            "email": "rorytest123@gmail.com",
            "location": "Dundalk",
            "password": "Test1234567!",
            "confirm_password": "Test1234567!",
            "user_type": "helper",  
        },
        follow_redirects=False,
    )

 
    assert resp.status_code in (302, 303)
    assert "/home_page/" in resp.headers["Location"]

    with app.app_context():
        user = Users.query.filter_by(email="rorytest123@gmail.com").first()
        assert user is not None
        assert user.name == "Rory OGorman"
        assert user.work_area == "Dundalk"
        assert user.type == "helper"