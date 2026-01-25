from flask import Blueprint, render_template, request, jsonify
from db.database import db
from db.models import Communities, Users
messages_blueprint = Blueprint("messages", __name__, template_folder="templates")


@messages_blueprint.route("/inbox/")
def inbox_page():
    return render_template("/messages/inbox.html")


@messages_blueprint.route("/message_chat/")
def message_chat():
    return render_template("/messages/message_chat.html")

@messages_blueprint.route("/temp_inbox/")
def temp_inbox_page():
    return render_template("/messages/temp_inbox.html")   