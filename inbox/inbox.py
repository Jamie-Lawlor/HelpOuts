from flask import Blueprint, render_template

inbox_blueprint = Blueprint(
    "inbox", __name__, static_folder="static", template_folder="templates"
)


@inbox_blueprint.route("/")
def inbox():
    return render_template("inbox.html")
