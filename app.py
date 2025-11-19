from flask import Flask, render_template, redirect
import os
from db.database import db
from db.modals import Users
from flask_migrate import Migrate
from routes.login import login_blueprint
from routes.messages import messages_blueprint
from routes.profile import profile_blueprint
from routes.posts import posts_blueprint
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.secret_key = os.getenv("SECRET_KEY")


db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(login_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(posts_blueprint)


@app.route("/testDb")
def test_db():
    users = Users.query.all()
    return "<br>".join([user.name for user in users])


@app.route("/addTestUser")
def add_test_user():
    user = Users(
        name="Test User3",
        email="test3@test3.com",
        password="Test1234567!",
        type="helpee",
        work_area="Louth",
        specialism=None,
        skills=None,
        rating=None,
    )
    db.session.add(user)
    db.session.commit()
    return redirect("/testDb")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home_page/")
def home_page():
    return render_template("home_page.html")


@app.route("/settings/")
def settings_page():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)
