from flask import Blueprint, render_template, request, redirect, session,jsonify
from db.database import db
from db.models import Users, Communities
from werkzeug.security import generate_password_hash
import re

login_blueprint = Blueprint("login", __name__, template_folder="templates")

@login_blueprint.route("/login/")
def login():
    return render_template("login/login.html")

@login_blueprint.route("/register_page/")
def register_page():
    return render_template("login/register_account.html")


@login_blueprint.route("/helper_register_page/")
def helper_register_page():
    return render_template("login/helper_register_account.html")


@login_blueprint.route("/register", methods=["POST"])
def register_helpee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    location = request.form.get("location")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    user_type = request.form.get("user_type")
    if request.form.get("community_name") is not None:
        community_name = request.form.get("community_name")
        if_exists = Communities.query.filter_by(name = community_name).first()
        if if_exists:
            error = "A community with this name already exists"
            return render_template("login/register_account.html", error=error)
        else:
            community = Communities(
            name=community_name,
            area=location,
            description="",
            profile_picture="",
        )
            db.session.add(community)
            db.session.commit()
            session["community_id"] = community.id
            return redirect("/home_page/")
    # check if this users already exists
    else:
        if_exists = Users.query.filter_by(email=email).first()
        if if_exists:
            # this error message is passed to the frontend and can be used to display an error to the user
            error = "A user with this email already exists"
            return render_template("login/register_account.html", error=error)

        # validate password & user details

        # https://mailtrap.io/blog/flask-contact-form/#Custom-Validation-Functions - custom validation
        if not first_name or not last_name or not email or not location or not password:
            error = "All Fields Must Be Filled Out"
            return render_template("login/register_account.html", error=error)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid Email Entered, Please Enter an Email Like 'example@gmail.com'"
            return render_template("login/register_account.html", error=error)

        # password regular expression
        if len(password) < 8:
            error = "Invalid Password Entered, Must be More than 8 Characters"
            return render_template("login/register_account.html", error=error)
        if not re.search(r"[A-Z]", password):
            error = "Invalid Password Entered, Must have a Uppercase Letter"
            return render_template("login/register_account.html", error=error)
        if not re.search(r"[a-z]", password):
            error = "Invalid Password Entered, Must have a Lowercase Letter"
            return render_template("login/register_account.html", error=error)
        if not re.search(r"[0-9]", password):
            error = "Invalid Password Entered, Must have a Number"
            return render_template("login/register_account.html", error=error)

        if confirm_password != password:
            error = "Passwords Do Not Match, Please Try Again"
            return render_template("login/register_account.html", error=error)

        hashed_password = generate_password_hash(password)

        # key = RSA.generate(2048)
        # private_key = key
        # public_key = key.public_key

        user = Users(
            name=first_name + " " + last_name,
            email=email,
            password=hashed_password,
            type=user_type,
            work_area=location,
            rating=0,
            # private_key = private_key,
            # public_key = public_key
        )
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect("/home_page/")


@login_blueprint.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

#Remove when no longer needed as test
@login_blueprint.route("/test_login_user", methods=["POST"])
def test_login_user():
    user_id = int(request.json["data"])
    user_data = Users.query.get_or_404(user_id)
    session["user_id"] = user_id
    session["profile_picture"] = user_data.profile_picture
    dataArray = [str(session["user_id"]), session["profile_picture"]]
    print(user_data.profile_picture)
    return jsonify(dataArray)

#Remove when no longer needed as test
@login_blueprint.route("/test_login_admin", methods=["POST"])
def test_login_admin():
    community_id = int(request.json["data"])
    community_data = Communities.query.get_or_404(community_id)
    session["community_id"] = community_id
    session["profile_picture"] = community_data.profile_picture
    dataArray = [str(session["community_id"]), session["profile_picture"]]
    print(community_data.profile_picture)
    return jsonify(dataArray)