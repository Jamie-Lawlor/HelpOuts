from flask import Blueprint, render_template

add_post_blueprint = Blueprint(
    "add_post", __name__, static_folder="static", template_folder="templates"
)


@add_post_blueprint.route("/")
def add_post_page():
    return render_template("add_post.html")
