from flask import Blueprint, render_template, request, redirect
from db.database import db
from db.modals import Users
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
        return render_template("/register_helpee/", error=error) 
    
    # validate password & user details
    
    
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
