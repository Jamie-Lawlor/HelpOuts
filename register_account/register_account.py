from flask import Blueprint, render_template

register_account_blueprint = Blueprint(
    "register_account", __name__, static_folder="static", template_folder="templates"
)


@register_account_blueprint.route("/")
def register_page():
    return render_template("register_account.html")
