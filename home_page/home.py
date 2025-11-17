from flask import Blueprint, render_template

home_blueprint = Blueprint(
    "home_page", __name__, static_folder="static", template_folder="templates"
)


@home_blueprint.route("/")
def home_page():
    return render_template("home_page.html")
