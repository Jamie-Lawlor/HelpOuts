import os
import tempfile
import pytest

from db.database import db
from db.models import Users, Communities


@pytest.fixture
def app():
    # Your Flask app lives in app.py
    from app import app as flask_app

    # Create a temporary sqlite DB file
    db_fd, db_path = tempfile.mkstemp()
    test_db_uri = "sqlite:///" + db_path

    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=test_db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret",
    )

    assert flask_app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///")

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def community(app):
    c = Communities(
        name="Test Community",
        area="Test Area",
        description="A test community",
        profile_picture="https://example.com/community.png",
    )
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture
def user(app, community):
    u = Users(
        name="Test User",
        email="test@example.com",
        password="Valid1!x",  # must pass your model password validator
        type="helpee",
        private_key=b"\x01" * 32,
        public_key=b"\x02" * 32,
        community_id=community.id,
        profile_picture="https://example.com/user.png",
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def logged_in_client(client, user):
    # your app appears to use session["id"] for logged-in user
    with client.session_transaction() as sess:
        sess["id"] = user.id
    return client
