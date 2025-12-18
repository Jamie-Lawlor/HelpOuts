from flask import Blueprint, render_template

profile_blueprint = Blueprint("profile", __name__, template_folder="templates")


@profile_blueprint.route("/user_profile/")
def inbox_page():
    return render_template("/profile/community_profile.html")
