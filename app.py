from flask import Flask, render_template, redirect, session
import os
from db.database import db
from db.modals import Users, Messages
from flask_migrate import Migrate
from routes.login import login_blueprint
from routes.messages import messages_blueprint
from routes.profile import profile_blueprint
from routes.posts import posts_blueprint
from routes.subscriptions import subscriptions_blueprint
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, leave_room, send
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

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on("join_room")
def handle_connect(data):
    user = data["user"]
    room = data["room"]
    join_room(room)
    send(user + ' has entered the room.', to=room)
    print(user + " has joined the room. ")

# @socketio.on("join")
# def on_join(data):
#     username = 


# @socketio.on("message_sent")
# def message_sent(message):
#     # message = Messages(
#     #     sender_id=session.get("id"),
#     #     reciever_id=5,
#     #     content=message
#     # )
#     # db.session.add(message)
#     # db.session.commit()
#     print("id: ",session.get("id"))
#     print("Here is your message: ", message)
#     socketio.emit('display_message', message)

if __name__ == "__main__":
    socketio.run(app, debug=True)
