from flask import Flask, render_template
import os
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

app.secret_key = "TODO_BAD_SECRET_KEY" 

from db.database import db
from db.modals import Users


# migrate = Migrate(app.db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home_page")
def home_page():
    return render_template("home_page.html")


@app.route("/add_post")
def add_post_page():
    return render_template("add_post.html")


@app.route("/inbox")
def inbox():
    return render_template("inbox.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/user_profile")
def user_profile_page():
    return render_template("user_profile.html")


if __name__ == "__main__":
    app.run(debug=True)



