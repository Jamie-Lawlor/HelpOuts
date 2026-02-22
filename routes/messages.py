from flask import Blueprint, render_template, request, jsonify, session
from db.database import db
from db.models import Communities, Users
messages_blueprint = Blueprint("messages", __name__, template_folder="templates")


@messages_blueprint.route("/inbox/")
def inbox_page():
    if session.get("community_id") is not None:
        community_id = int(session["community_id"])
        all_users = Users.query.where(community_id == community_id).all()
        return render_template("/messages/inbox.html", all_users = all_users)
    else:
        user_id = int(session["user_id"])
        user = Users.query.get_or_404(user_id)
        community = Communities.query.get_or_404(user.community_id)
        communityArray = [community]
        return render_template("/messages/inbox.html", users_community = communityArray)

@messages_blueprint.route("/message_chat/", methods=["POST"])
def message_chat():
    id = request.form.get("id")
    if session.get("community_id") is not None:
        user = Users.query.get_or_404(id)
        userArray = [user, session["community_id"]]
        return render_template("/messages/message_chat.html", user = userArray)
    else:
        community = Communities.query.get_or_404(id)
        communityArray = [community, session["user_id"]]
    return render_template("/messages/message_chat.html", community = communityArray)

@messages_blueprint.route("/temp_inbox/")
def temp_inbox_page():
    return render_template("/messages/temp_inbox.html")   

@messages_blueprint.route("/generate_keys", methods=["POST"])
def generate_keys():
    data = request.get_json()
    # print(data)
    private_key = data["private_key"]
    public_key = data["public_key"]

    # user_id = session["id"]
    sender_id = 3 # 
    receiver_id = 2 # Ryan

    sender = Users.query.get_or_404(3)
    receiver = Users.query.get_or_404(2)

    if sender is None:
        return render_template("/messages/inbox.html")
    if receiver is None:
        render_template("/messages/inbox.html")

    sender.public_key = public_key.encode('utf-8')
    receiver.private_key = private_key.encode('utf-8')
    db.session.commit()
    
    print(public_key)
    return f"{private_key}, {public_key}"