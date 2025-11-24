from flask import Blueprint, render_template, request, redirect
from db.database import db
from db.modals import Users
import re
login_blueprint = Blueprint("login", __name__, template_folder="templates")


@login_blueprint.route("/register_page/")
def register_page():
    return render_template("login/register_account.html")


@login_blueprint.route("/helper_register_page/")
def helper_register_page():
    return render_template("login/helper_register_account.html")


@login_blueprint.route("/register_helpee", methods=["POST"])
def register_helpee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    location = request.form.get("location")
    password = request.form.get("password")
    
    
    # check if this users already exists
    if_exists = Users.query.filter_by(email=email).first()
    if if_exists:
        # this error message is passed to the frontend and can be used to display an error to the user
        error = "A user with this email already exists"
        return render_template("login/register_account.html", error=error)
    
    # validate password & user details

    # https://mailtrap.io/blog/flask-contact-form/#Custom-Validation-Functions - custom validation
    if not first_name or not last_name or not email or not location or not password:
        error = "All Fields Must Be Filled Out"
        return render_template("/register_helpee/", error=error)
    

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error = "Invalid Email Entered, Please Enter an Email Like 'example@gmail.com'"
        return render_template("/register_helpee/", error=error)
    
    # https://uibakery.io/regex-library/password - password regular expression
    if not re.match(r"/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/", password):
        error = "Invalid Password Entered, Please Enter a Password that Includes a Minimum of 8 Characters, at least One Uppercase Letter, One Lowercase Letter, One Number and One Special Character"
        return render_template("/register_helpee/", error=error)
    
    user = Users(
        name=first_name + " " + last_name,
        email=email,
        password=password,
        type="helpee",
        work_area=location,
        rating=0
        )
    db.session.add(user)
    db.session.commit()
    
    return redirect("/home_page/")
