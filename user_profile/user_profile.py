from flask import Blueprint, render_template

user_profile_blueprint = Blueprint(
    "user_profile", __name__, static_folder="static", template_folder="templates"
)


@user_profile_blueprint.route("/")
def user_profile_page():
    return render_template("user_profile.html")
