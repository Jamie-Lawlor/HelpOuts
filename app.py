from flask import Flask, render_template, session, send_file, request, redirect, jsonify
from flask_mail import Mail, Message
import os
from db.database import db
from db.models import Users, Jobs, Projects, Communities
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
import pyotp

load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["MAIL_SERVER"] = os.getenv("GMAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("GMAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("GMAIL_TLS") == "True"
sender = app.config["MAIL_USERNAME"] = os.getenv("GMAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_PASSWORD")


app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)
socketio.init_app(app)
mail = Mail(app)

migrate = Migrate(app, db)
app.register_blueprint(login_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(subscriptions_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api")


# context processor runs before the template is loaded, making api key
# global so its available in base.html
# https://flask.palletsprojects.com/en/stable/api/#flask.Flask.context_processor
@app.context_processor
def inject_gmaps_key():
    return dict(GMAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest.json")


@app.route("/manifest.json")
def serve_PWA_service_worker():
    return send_file("sw.js", mimetype="application/javascript")


@app.route("/")
def index():
    # DELETE THIS WHEN DONE
    # session["user_id"] = 3
    return render_template("index.html")


@app.route("/home_page/")
def home_page():
    if 'type' in session: 
        vapid_key = os.getenv("VAPID_PUBLIC_KEY_BASE_64")
        return render_template("home_page.html", vapid_key = vapid_key)         
    else:
        return redirect("/")

@app.route("/get_jobs")
def get_jobs():
        if session["type"]=="helper":
            helper_data = Users.query.get_or_404(session["user_id"])
            job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == helper_data.community_id).all()
            dataArray=[]
            for jobs in job_data:
                dataArray.append(jobs.to_dict())
            return jsonify(dataArray)
        return jsonify("SKIP")   


@app.route("/settings/")
def settings_page():
    return render_template("settings.html")


@app.route("/helper_settings/")
def helper_settings_page():
    return render_template("helper_settings.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = Users.query.filter_by(email=email).first()
    # hashed_password = user.password
    # password_check = check_password_hash(hashed_password, password)

    if user is not None:
        hashed_password = user.password
        password_check = check_password_hash(hashed_password, password)

    if user is not None and password_check:
        session["email"] = email
        session.pop("otp", None)
        return redirect("/mfa")
    else:
        error = "Email or Password Is Incorrect"
        return render_template("login/login.html", error=error)


@app.route("/mfa", methods=["GET", "POST"])
def mfa():
    if "email" not in session:
        return redirect("/login")
    
    user = Users.query.filter_by(email=session["email"]).first()
    
    if request.method == "POST":
        otp = request.form["otp"]
        mfa_session = session.get("otp")
        
        if mfa_session:
            totp = pyotp.TOTP(mfa_session)
            if totp.verify(otp):
                session.pop("email", None)
                session["user_id"] = user.id
                # TODO profile picture comes from S3 now, not the database
                session["profile_picture"] = user.profile_picture
                session["type"] = user.type
                return redirect("/home_page/")
        else:
            error = "Incorrect One Time Password, Please Try Again."
            return render_template("login/mfa.html", error = error)
    

    if "otp" not in session:
        pyotp_secret = pyotp.random_base32()
        session["otp"] = pyotp_secret

        totp = pyotp.TOTP(pyotp_secret)
        otp_code = totp.now()

        message = Message("HelpOuts Verification", sender=sender, recipients=[user.email])
        message.body = f"Your One Time Passcode is: {otp_code}"
        mail.send(message)
    
    return render_template("login/mfa.html")

@app.route("/get_type", methods=["GET"])
def get_type():
    return session["type"]

@app.route("/communityTestMap")
def community_test_map():
    community_id=1
    return render_template("test_space/test_community_map.html", community_id=1, GMAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY"))

if __name__ == "__main__":
    socketio.run(app, debug=True)
