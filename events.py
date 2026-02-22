from extensions import socketio
from flask import session
from flask_socketio import join_room, send
from db.database import db
from db.models import Users, Messages, Communities
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


@socketio.on("join_room")
def handle_connect():
    session["room"] = "user_3_user_5_direct_messaging"
    room = session.get("room")
    join_room(room)



@socketio.on("message_sent")
def message_sent(data):
    date = datetime.now()
    room = session.get("room")
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    sender_of_message = data["sender"]

    # sender = Users.query.get_or_404(2)
    # receiver = Users.query.get_or_404(2)
    if sender_of_message == "community":
        sender_data = Communities.query.get_or_404(sender_id)
    else:
        sender_data = Users.query.get_or_404(sender_id)
    
    message = data["message"]
    #DELETE THE BELOW LINE WHEN ENCRYPTION IS FIXED
    binary_message = message.encode('utf-8')

    # public_key = sender.public_key

    # RSA_public_key = RSA.import_key(public_key)
    # cipher = PKCS1_OAEP.new(RSA_public_key)
    # encrypted_message = cipher.encrypt(message.encode('utf-8'))
#
    messageContent = {
        "user": sender_data.name,
        "message": message,
        "sent": date.strftime("%H:%M"),
        "profile_picture":sender_data.profile_picture
    }
    message = Messages(
        sender_id=int(sender_id),
        receiver_id=int(receiver_id),
        # content=encrypted_message,
        content=binary_message,
        timestamp = date
    )
    db.session.add(message)
    db.session.commit()
    send(messageContent, to = room)

