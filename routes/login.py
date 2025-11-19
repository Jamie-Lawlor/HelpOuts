from flask import Blueprint, render_template, request, redirect

login_blueprint = Blueprint("login", __name__, template_folder="templates")


@login_blueprint.route("/register_page")
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
    return redirect("/home_page/")
