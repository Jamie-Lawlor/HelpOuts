from flask import Blueprint, render_template

settings_blueprint = Blueprint(
    "settings", __name__, static_folder="static", template_folder="templates"
)


@settings_blueprint.route("/")
def settings():
    return render_template("settings.html")
