import io
from PIL import Image
import pytest

from db.database import db
from db.models import Users


def make_test_image_file():
    """Create an in-memory valid JPEG file that Flask treats like an upload."""
    img = Image.new("RGB", (10, 10))
    file_obj = io.BytesIO()
    img.save(file_obj, format="JPEG")
    file_obj.seek(0)
    return file_obj


def test_update_profile_picture_user_not_found(client, app):
    with client.session_transaction() as sess:
        sess["id" ] = 9999

    img_file = make_test_image_file()

    resp = client.post(
        "/api/updateProfilePicture",
        data={"image": (img_file, "pic.jpg")},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 404
    assert resp.get_json()["error"] == "User not found"


def test_update_profile_picture_no_image_uploaded(client, app):
    with app.app_context():
        u = Users(
            name="Test User",
            email="testuser@example.com",
            password="Test1234567!",
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="",
        )
        db.session.add(u)
        db.session.commit()
        user_id = u.id

    with client.session_transaction() as sess:
        sess["id"] = user_id

    resp = client.post(
        "/api/updateProfilePicture",
        data={}, 
        content_type="multipart/form-data",
    )

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "No image uploaded"


def test_update_profile_picture_success_updates_db(client, app, monkeypatch):
    with app.app_context():
        u = Users(
            name="Test User",
            email="testuser2@example.com",
            password="Test1234567!",
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="",
        )
        db.session.add(u)
        db.session.commit()
        user_id = u.id

    with client.session_transaction() as sess:
        sess["id"] = user_id

    class FakeResponse:
        def json(self):
            return {
                "verdict": "real",
                "confidence": 0.99,
                "label": "human",
            }

    def fake_requests_post(*args, **kwargs):
        return FakeResponse()

    import routes.api as api_module
    monkeypatch.setattr(api_module.requests, "post", fake_requests_post)

    def fake_upload_fileobj(*args, **kwargs):
        return None

    monkeypatch.setattr(api_module.s3, "upload_fileobj", fake_upload_fileobj)

    img_file = make_test_image_file()

    resp = client.post(
        "/api/updateProfilePicture",
        data={"image": (img_file, "pic.jpg")},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    data = resp.get_json()

    assert data["message"] == "Image uploaded successfully"
    assert data["user_id"] == user_id
    assert data["verdict"] == "real"
    assert data["label"] == "l"

    with app.app_context():
        updated = Users.query.get(user_id)
        assert updated.profile_picture is not None
        assert updated.profile_picture != ""