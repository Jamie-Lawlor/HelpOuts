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
    form_data = request.json["form_data"]
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


@posts_blueprint.route("/edit_post", methods=["POST"])
def edit_post():
    updated_data = request.json["edit_data"]
    updated_title = updated_data[1]
    updated_description = updated_data[2]
    updated_area = updated_data[3]
    
    updated_job=Jobs.query.filter_by(id=updated_data[0]).first()
    updated_job.job_title = updated_title
    updated_job.job_description = updated_description
    updated_job.area = updated_area
    updated_job.created_date = db.func.current_timestamp()
    db.session.commit()
    return ""

@posts_blueprint.route("/delete_post", methods=["POST"])
def delete_post():
    updated_data = int(request.json["post_id"])
    
    db.session.delete(Jobs.query.filter_by(id=updated_data).first())
    db.session.commit()
    return ""