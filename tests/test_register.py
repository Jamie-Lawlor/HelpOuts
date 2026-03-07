import io
from PIL import Image
from db.models import Users


def make_test_image():
    img = Image.new("RGB", (50, 50), color="red")
    file = io.BytesIO()
    img.save(file, "JPEG")
    file.seek(0)
    return file


def test_register_adds_user_to_database(client, app, monkeypatch):

    class FakeResponse:
        def json(self):
            return {
                "verdict": "real",
                "confidence": 0.99,
                "label": "human"
            }

    import routes.login as login_module
    monkeypatch.setattr(login_module.requests, "post", lambda *a, **k: FakeResponse())

    img = make_test_image()

    resp = client.post(
        "/register",
        data={
            "first_name": "Rory",
            "last_name": "OGorman",
            "email": "rorytest123@gmail.com",
            "phone": "0850000000",
            "location": "Dundalk",
            "password": "Test1234567!",
            "confirm_password": "Test1234567!",
            "user_type": "helper",
            "image": (img, "test.jpg"), 
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert resp.status_code in (302, 303)

    with app.app_context():
        user = Users.query.filter_by(email="rorytest123@gmail.com").first()
        assert user is not None