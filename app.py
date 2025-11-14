from flask import Flask, render_template

app = Flask(__name__)


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


@app.route("/register_page")
def register_page():
    return render_template("register_account.html")


@app.route("/helper_register_page")
def helper_register_page():
    return render_template("helper_register_account.html")


if __name__ == "__main__":
    app.run(debug=True)
