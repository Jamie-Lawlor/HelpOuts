import sys
import os
import pytest
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import db

@pytest.fixture
def app():
    flask_app = Flask(__name__)

    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret",
    )

    db.init_app(flask_app)

    # Register blueprints (same as app.py)
    from routes.login import login_blueprint
    from routes.messages import messages_blueprint
    from routes.profile import profile_blueprint
    from routes.posts import posts_blueprint
    from routes.subscriptions import subscriptions_blueprint

    flask_app.register_blueprint(login_blueprint)
    flask_app.register_blueprint(messages_blueprint)
    flask_app.register_blueprint(profile_blueprint)
    flask_app.register_blueprint(posts_blueprint)
    flask_app.register_blueprint(subscriptions_blueprint)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def community(app):
    from db.models import Communities
    c = Communities(
        id=1,  # create_project hardcodes community_id=1
        name="Dundalk Tidy Towns",
        area="Dundalk, Co.Louth",
        description="Test community",
        profile_picture="/static/images/community_image.png",
    )
    db.session.add(c)
    db.session.commit()
    return c
