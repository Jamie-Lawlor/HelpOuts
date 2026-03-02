import sys
import os
import pytest
from flask import Flask, send_file

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import db


@pytest.fixture
def app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    static_dir = os.path.join(project_root, "static")
    templates_dir = os.path.join(project_root, "templates")

    flask_app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret",
    )

    db.init_app(flask_app)

    from routes.login import login_blueprint
    from routes.messages import messages_blueprint
    from routes.profile import profile_blueprint
    from routes.posts import posts_blueprint
    from routes.subscriptions import subscriptions_blueprint
    from routes.api import api_blueprint

    flask_app.register_blueprint(login_blueprint)
    flask_app.register_blueprint(messages_blueprint)
    flask_app.register_blueprint(profile_blueprint)
    flask_app.register_blueprint(posts_blueprint)
    flask_app.register_blueprint(subscriptions_blueprint)
    flask_app.register_blueprint(api_blueprint, url_prefix="/api")

   
    @flask_app.route("/manifest.json")
    def manifest():
        return send_file(os.path.join(project_root, "manifest.json"), mimetype="application/manifest+json")

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()