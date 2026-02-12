from flask import Flask, render_template, session, send_file
import os
from db.database import db
from flask_migrate import Migrate
from routes.login import login_blueprint
from routes.messages import messages_blueprint
from routes.profile import profile_blueprint
from routes.posts import posts_blueprint
from routes.subscriptions import subscriptions_blueprint
from dotenv import load_dotenv
from events import socketio
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)
socketio.init_app(app)

migrate = Migrate(app, db)
app.register_blueprint(login_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(subscriptions_blueprint)

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype = 'application/manifest.json')

@app.route('/manifest.json')
def serve_PWA_service_worker():
    return send_file('sw.js', mimetype = 'application/javascript')

@app.route("/")
def index():
    session["id"] = 3
    return render_template("index.html")


@app.route("/home_page/")
def home_page():
    return render_template("home_page.html")


@app.route("/settings/")
def settings_page():
    return render_template("settings.html")


@app.route("/helper_settings/")
def helper_settings_page():
    return render_template("helper_settings.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
