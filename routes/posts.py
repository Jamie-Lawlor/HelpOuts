from flask import Blueprint, render_template, request, redirect, session, jsonify
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
    form_data = request.json["formData"]
    title = form_data[0]
    description = form_data[1]
    area = form_data[2]
    
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
    job_data = Jobs.query.get_or_404(new_job.id)
    return jsonify(job_data.to_dict())


@posts_blueprint.route("/view_post/<post_id>")
def view_specific_post_page(post_id):
    job_data = Jobs.query.get_or_404(post_id).to_dict()
    return render_template("/posts/view_post.html", job_data = job_data)


# @posts_blueprint.route("/retrieve_job_data", methods=["POST"])
# def retrieve_data()