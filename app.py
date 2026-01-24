from flask import Flask, render_template, redirect, session
import os
from db.database import db
from db.models import Users, Messages, Communities
from flask_migrate import Migrate
from routes.login import login_blueprint
from routes.messages import messages_blueprint
from routes.profile import profile_blueprint
from routes.posts import posts_blueprint
from routes.subscriptions import subscriptions_blueprint
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, leave_room, send
import datetime
from base64 import b64encode, b64decode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.secret_key = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(login_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(subscriptions_blueprint)


@app.route("/")
def index():
    session["id"] = 3
    return render_template("index.html")


@app.route("/home_page/")
def home_page():
    return render_template("home_page.html")


@app.route("/settings/")
def settings_page():
    return render_template("settings.html")


@app.route("/helper_settings/")
def helper_settings_page():
    return render_template("helper_settings.html")


@socketio.on("join_room")
def handle_connect():
    session["room"] = "user_3_user_5_direct_messaging"
    room = session.get("room")
    join_room(room)



@socketio.on("message_sent")
def message_sent(data):
    date = datetime.datetime.now()
    room = session.get("room")
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    if sender_id == "1":
        sender_data = Communities.query.get_or_404(sender_id)
    else:
        sender_data = Users.query.get_or_404(sender_id)
    
    message = data["message"].encode()

    #Encryption
    aes_encryption_key = get_random_bytes(32)
    iv = get_random_bytes(16)
    encryption_cipher = AES.new(aes_encryption_key, AES.MODE_GCM, nonce=iv)
    encrypted_message = encryption_cipher.encrypt_and_digest(message)
    
    receiver_information = Users.query.get_or_404(receiver_id)
    receiver_public_key = RSA.import_key(receiver_information.public_key)
    public_rsa_key = PKCS1_OAEP.new(receiver_public_key)
    encrypted_key = public_rsa_key.encrypt(aes_encryption_key)

    #Decryption
    iv_encrypted = b64decode(data["iv"])

    receiver_private_key = RSA.import_key(receiver_information.private_key)
    private_rsa_key = PKCS1_OAEP.new(receiver_private_key)
    decrypted_key = private_rsa_key.decrypt(encrypted_key)

    decryption_cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=iv_encrypted)
    decrypted_message = decryption_cipher.decrypt_and_verify(encrypted_message)

    messageContent = {
        "user": sender_data.name,
        "message": decrypted_message.decode('utf-8'),
        "sent": date.strftime("%H:%M"),
        "profile_picture":sender_data.profile_picture
    }
    message = Messages(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=b64encode(encrypted_message).decode('utf-8'),
        aes_key = b64encode(encrypted_key).decode('utf-8'),
        iv = b64encode(iv).decode('utf-8'),
        timestamp = db.func.current_timestamp()
    )
    db.session.add(message)
    db.session.commit()
    send(messageContent, to = room)

if __name__ == "__main__":
    socketio.run(app, debug=True)
