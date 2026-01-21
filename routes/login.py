from flask import Blueprint, render_template, request, redirect
from db.database import db
from db.models import Users
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
    confirm_password = request.form.get("confirm_password")
    
    
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
        return render_template("login/register_account.html", error=error)
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error = "Invalid Email Entered, Please Enter an Email Like 'example@gmail.com'"
        return render_template("login/register_account.html", error=error)
    
    # password regular expression 
    if len(password) < 8:
        error = "Invalid Password Entered, Must be More than 8 Characters"
        return render_template("login/register_account.html", error=error)
    if not re.search(r'[A-Z]', password):
        error = "Invalid Password Entered, Must have a Uppercase Letter"
        return render_template("login/register_account.html", error=error)
    if not re.search(r'[a-z]', password):
        error = "Invalid Password Entered, Must have a Lowercase Letter"
        return render_template("login/register_account.html", error=error)
    if not re.search(r'[0-9]', password):
        error = "Invalid Password Entered, Must have a Number"
        return render_template("login/register_account.html", error=error)
        
    if confirm_password != password:
        error = "Passwords Do Not Match, Please Try Again"
        return render_template("login/register_account.html", error=error)
    
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
