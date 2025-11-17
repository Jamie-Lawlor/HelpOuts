from flask import Blueprint, render_template

helper_register_account_blueprint = Blueprint(
    "helper_register_account",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@helper_register_account_blueprint.route("/")
def helper_register_page():
    return render_template("helper_register_account.html")
