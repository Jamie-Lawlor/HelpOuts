from flask import Blueprint, render_template

posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/add_post/")
def post_page():
    return render_template("/posts/add_post.html")
