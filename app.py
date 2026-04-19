from flask import Flask, render_template, session, send_file, request, redirect, jsonify
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user
import os
from db.database import db
from db.models import Users, Jobs, Projects, Communities, Logs
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
login_manager = LoginManager(app)
login_manager.login_view = 'index'
mail = Mail(app)

migrate = Migrate(app, db)
app.register_blueprint(login_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(subscriptions_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api")

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# context processor runs before the template is loaded, making api key
# global so its available in base.html
# https://flask.palletsprojects.com/en/stable/api/#flask.Flask.context_processor
@app.context_processor
def inject_gmaps_key():
    return dict(GMAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY"), AWS_BUCKET=os.getenv("AWS_S3_BASE_URL"))

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
        if session['type'] == "helper":
            helper_data = Users.query.get_or_404(session["user_id"])
            return render_template("home_page.html", vapid_key = vapid_key, helper_data = helper_data)    
        else:
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
        
        db.session.commit()
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
            if totp.verify(otp, valid_window = 2):
                login_user(user)
                session.pop("email", None)
                session["user_id"] = user.id
                session["user_name"] = user.name
                print(user.community_id)
                if user.community_id is not None:
                    community = Communities.query.join(Users, Communities.id == Users.community_id).where(Communities.id == user.community_id).first()
                    session['community_name'] = community.name
                else:
                    session['community_name'] = None
                # TODO profile picture comes from S3 now, not the database
                session["profile_picture"] = user.profile_picture
                session["type"] = user.type
                logs = Logs(
                    user_id = session["user_id"],
                    action = "Logged In (MFA)",
                    target = "Session"
                )
                db.session.add(logs)
                if session["type"] == "chairperson":
                    community = Communities.query.join(Users, Communities.id == Users.community_id).where(Users.type == "chairperson").first()
                    print(community.name)
                    return redirect(f"/community_profile/{ community.name }")
                else:
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
        message.body = f"Your HelpOuts One Time Passcode is: {otp_code}"
        message.html = f"""
            <html>
                <body>
                <table style="width: 100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                        <td style="width: 60px;">
                            <img
                                src="cid:helpouts_logo"
                                alt="Helpouts logo"
                                style="width: 200%;"
                            />
                        </td>
                        <td style="padding-left: 40px;">
                            <h2 style="color: #3d6978; font-weight: bold; font-family: 'Source Serif 4', serif;">HelpOuts Verification Code</h2>
                        </td>
                    </tr>
                </table>
                    <p>Please use the code below to complete your login. </p><p style="font-weight: bold;">It will expire in 2 minutes:</p>
                    <div style="background-color: #f8f9fa; padding: 20px; text-align: center; font-weight: bold; font-size: 28px">{otp_code}</div>
                    <div style="border-top: 2px solid #8a8c8f; margin-bottom: 10px;">
                    <p style="color: #6c757d">If you did not login in, please disregard this email</p>
                    </div>
                </body>
            </html>
        """
        filename = "static/images/templogo6.png" 
        with open(filename, "rb") as fp:
            message.attach(
                filename="templogo6.png",
                content_type= "image/png",
                data=fp.read(),
                disposition="inline",
                headers={"Content-ID": "<helpouts_logo>"}
            )
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
