from flask import Blueprint, render_template, request, redirect, session
from db.database import db
from db.modals import Jobs
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
    
    
    # Security & Validation 
    
    
    # We get the id from the session which is set when the user logs in
    new_job = Jobs(
        helpee_id=3,
        status="NA", # Not Accepted as default
        area=area,
        job_title=title,
        job_description=description,
        short_title="",
        short_type="",
    )
    
    db.session.add(new_job)
    db.session.commit()
    return redirect("/view_post/")
