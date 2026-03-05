import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def app(monkeypatch):


    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

    import importlib
    import app as app_module
    importlib.reload(app_module) 

    flask_app = app_module.app

    from db.database import db
    with flask_app.app_context():
        db.drop_all()
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()