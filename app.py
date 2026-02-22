from flask import Flask, render_template, session, send_file, request, redirect
import os
from db.database import db
from db.models import Users
from flask_migrate import Migrate
from routes.login import login_blueprint
from routes.messages import messages_blueprint
from routes.profile import profile_blueprint
from routes.posts import posts_blueprint
from routes.subscriptions import subscriptions_blueprint
from routes.api import api_blueprint
from werkzeug.security import check_password_hash
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
app.register_blueprint(api_blueprint, url_prefix="/api")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype = 'application/manifest.json')

@app.route('/manifest.json')
def serve_PWA_service_worker():
    return send_file('sw.js', mimetype = 'application/javascript')

@app.route("/")
def index():
    #DELETE THIS WHEN DONE
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

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = Users.query.filter_by(email = email).first()
    # hashed_password = user.password
    # password_check = check_password_hash(hashed_password, password)
    
    if user is not None:
        hashed_password = user.password
        password_check = check_password_hash(hashed_password, password)    

    if user is not None and password_check:
        session["user_id"] = user.id
        session["profile_picture"] = user.profile_picture
        return redirect("/home_page/")
    else:
        error = "Email or Password Is Incorrect"
        return render_template("login/login.html", error = error)

if __name__ == "__main__":
    socketio.run(app, debug=True)
