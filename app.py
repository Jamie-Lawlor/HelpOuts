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
from twilio.rest import Client
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.secret_key = os.getenv("SECRET_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
verify_sid = os.getenv("VERIFY_SID")
client = Client(account_sid, auth_token)
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
    otp_code = request.form.get("mfa")
    user = Users.query.filter_by(email = email).first()
    # hashed_password = user.password
    # password_check = check_password_hash(hashed_password, password)
    
    if user is not None:
        hashed_password = user.password
        password_check = check_password_hash(hashed_password, password)
        phone_number = user.phone_number
    
    otp_check = client.verify.v2.services(verify_sid).verification_checks.create(
        to=phone_number, code=otp_code
    )

    if user is not None and password_check and otp_check.status == "approved":
        session["user_id"] = user.id
        session["profile_picture"] = user.profile_picture
        session["type"] = user.type
        return redirect("/home_page/")
    else:
        error = "Email or Password Is Incorrect"
        return render_template("login/login.html", error = error)

@app.route("/MFA",methods=["POST"])
def MFA():
    data = request.get_json()
    email = data.get("email")
    user = Users.query.filter_by(email = email).first()
    
    if user is not None:
        phone_number = user.phone_number

    otp_validation = client.verify.v2.services(verify_sid).verifications.create(
        to=phone_number, channel="sms"
    )

    return {"status": otp_validation.status, "sid": otp_validation.sid}

if __name__ == "__main__":
    socketio.run(app, debug=True)
