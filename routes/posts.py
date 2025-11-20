from flask import Blueprint, render_template, request, redirect

posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/add_post/")
def post_page():
    return render_template("/posts/add_post.html")


@posts_blueprint.route("/view_post/")
def view_post_page():
    return render_template("/posts/view_post.html")


@posts_blueprint.route("/create_post", methods=["POST"])
def create_post():
    title = request.form.get("helpout_title")
    description = request.form.get("helpout_description")
    area = request.form.get("helpout_area")
    return redirect("/view_post/")
