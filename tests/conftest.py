import pytest

@pytest.fixture
def app():
    # CHANGE this import to wherever your Flask app is created
    from app import app as flask_app

    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # very important for form tests
    )

    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
