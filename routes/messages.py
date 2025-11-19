from flask import Blueprint, render_template

messages_blueprint = Blueprint("messages", __name__, template_folder="templates")


@messages_blueprint.route("/inbox/")
def inbox_page():
    return render_template("/messages/inbox.html")
