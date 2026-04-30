from extensions import socketio
from flask import session
from flask_socketio import join_room, send
from db.database import db
from db.models import Users, Messages, Communities, UserKeys
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


@socketio.on("join_room")
def handle_connect():
    session["room"] = "user_3_user_5_direct_messaging"
    room = session.get("room")
    join_room(room)


def decrypt_message(private_key, encrypted_message):
      # private_key_bytes = base64.b64decode(private_key)
    # print(len(bytes(private_key)))
    print(private_key)
    RSA_private_key = RSA.import_key(private_key)
    decipher = PKCS1_OAEP.new(RSA_private_key)
    encrypted_message = base64.b64decode(encrypted_message)
    decrypted_message = decipher.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message

def encrypt_message(public_key, message):
    print(public_key)
    # print(len(bytes(public_key)))
    RSA_public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(RSA_public_key)
    encrypted_message = cipher.encrypt(message.encode('utf-8'))
    encrypted_message_final = base64.b64encode(encrypted_message).decode('ascii')
    # print(encrypted_message_final)
    return encrypted_message_final


@socketio.on("message_sent")
def message_sent(data):
    date = datetime.now()
    room = session.get("room")
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    sender_of_message = data["sender"]
    print(sender_id)
    print(receiver_id)
    print(sender_of_message)

    # before user_keys table
    # if sender_of_message == "community":
    #     sender_data = Users.query.join(Communities, Users.community_id == Communities.id).where(Users.type == "chairperson", Communities.id == session["community_id"]).first()
    # else:
    #     sender_data = Users.query.get_or_404(sender_id)

    if sender_of_message == "community":
        # get the key from the chairperson of the community by joining community to user to get the chairperson id, then to user keys from the user id
        # saves storing a seprate key for just the community.
        # In the future if we wanted to have multiple chairpersons then the community would have its own.
        sender_data = (Users.query
            .join(Communities, Users.community_id == Communities.id)
            .join(UserKeys, Users.id == UserKeys.user_id)
            .add_columns(UserKeys.private_key, UserKeys.public_key) #
            .where(
                Users.type == "chairperson", 
                Communities.id == session["community_id"]
            )
            .first()
        )
    else:
        # else join users to user keys on the user id
        sender_data = (
            Users.query
            .join(UserKeys, Users.id == UserKeys.user_id)
            .add_columns(UserKeys.private_key, UserKeys.public_key)
            .where(Users.id == sender_id)
            .first_or_404()
        )
    
    message = data["message"]

    
    public_key = sender_data.public_key
    private_key = sender_data.private_key
    
    # public_key_bytes = base64.b64decode(public_key)
    # RSA_public_key = RSA.import_key(public_key)
    # cipher = PKCS1_OAEP.new(RSA_public_key)
    encrypted_message = encrypt_message(public_key, message)
    decrypted_message = decrypt_message(private_key, encrypted_message)

    messageContent = {
        "user": sender_data.name,
        "message": decrypted_message,
        "sent": date.strftime("%H:%M"),
        "profile_picture":sender_data.profile_picture
    }
    message = Messages(
        sender_id=int(sender_id),
        receiver_id=int(receiver_id),
        content=encrypted_message,
        timestamp = date
    )
    db.session.add(message)
    db.session.commit()
    send(messageContent, to = room)