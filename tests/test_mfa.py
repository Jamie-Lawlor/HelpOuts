from werkzeug.security import generate_password_hash

from db.database import db
from db.models import Users


def test_login_redirects_to_mfa_and_sets_email_session(client, app):
    with app.app_context():
        u = Users(
            name="MFA User",
            email="mfauser@example.com",
            password=generate_password_hash("Test1234567!"),
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="default.png",
        )
        db.session.add(u)
        db.session.commit()

    resp = client.post(
        "/login",
        data={"email": "mfauser@example.com", "password": "Test1234567!"},
        follow_redirects=False,
    )

    assert resp.status_code in (302, 303)
    assert resp.headers["Location"].endswith("/mfa")
    with client.session_transaction() as sess:
        assert sess.get("email") == "mfauser@example.com"


def test_mfa_get_generates_otp_and_sends_email(client, app, monkeypatch):
    with app.app_context():
        u = Users(
            name="MFA User 2",
            email="mfauser2@example.com",
            password=generate_password_hash("Test1234567!"),
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="default.png",
        )
        db.session.add(u)
        db.session.commit()

    with client.session_transaction() as sess:
        sess["email"] = "mfauser2@example.com"
        sess.pop("otp", None)

  
    class FakeTOTP:
        def __init__(self, secret):
            self.secret = secret

        def now(self):
            return "123456"

        def verify(self, otp):
            return otp == "123456"

    import app as app_module
    monkeypatch.setattr(app_module.pyotp, "random_base32", lambda: "FIXEDSECRET")
    monkeypatch.setattr(app_module.pyotp, "TOTP", lambda secret: FakeTOTP(secret))


    sent = {}

    def fake_send(message):
        sent["subject"] = getattr(message, "subject", None)
        sent["body"] = getattr(message, "body", None)
        sent["recipients"] = getattr(message, "recipients", None)

    monkeypatch.setattr(app_module.mail, "send", fake_send)

    class FakeMessage:
        def __init__(self, subject, sender=None, recipients=None):
            self.subject = subject
            self.sender = sender
            self.recipients = recipients
            self.body = ""

    monkeypatch.setattr(app_module, "Message", FakeMessage)

    resp = client.get("/mfa")
    assert resp.status_code == 200

    with client.session_transaction() as sess:
        assert sess.get("otp") == "FIXEDSECRET"
    assert "subject" in sent
    assert "One Time Passcode" in (sent.get("body") or "")
    assert "123456" in (sent.get("body") or "")


def test_mfa_post_correct_otp_logs_user_in(client, app, monkeypatch):
    with app.app_context():
        u = Users(
            name="MFA User 3",
            email="mfauser3@example.com",
            password=generate_password_hash("Test1234567!"),
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="default.png",
        )
        db.session.add(u)
        db.session.commit()
        user_id = u.id

    with client.session_transaction() as sess:
        sess["email"] = "mfauser3@example.com"
        sess["otp"] = "FIXEDSECRET"

    class FakeTOTP:
        def __init__(self, secret):
            self.secret = secret

        def verify(self, otp):
            return otp == "123456"

    import app as app_module
    monkeypatch.setattr(app_module.pyotp, "TOTP", lambda secret: FakeTOTP(secret))

    resp = client.post("/mfa", data={"otp": "123456"}, follow_redirects=False)
    assert resp.status_code in (302, 303)
    assert resp.headers["Location"].endswith("/home_page/")

    with client.session_transaction() as sess:
        assert sess.get("user_id") == user_id
        assert sess.get("type") == "helper"
        assert sess.get("email") is None  