from flask import Blueprint, render_template, request, redirect, session, jsonify
from db.database import db
from db.modals import Jobs

posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/add_project/")
def project_page():
    return render_template("/posts/add_project.html")

@posts_blueprint.route("/add_job/")
def post_page():
    return render_template("/posts/add_job.html")

@posts_blueprint.route("/view_post/")
def view_post_page():
    return render_template("/posts/view_post.html")


@posts_blueprint.route("/create_project", methods=["POST"])
def create_project():
    title = request.form.get("title")
    print("TITLE: ",title)
    description = request.form.get("description")
    print("DESCRIPTION: ",description)
    project_type = request.form.get("type")
    print("TYPE: ",project_type)
    helpers = request.form.get("helpers")
    print("HELPERS: ",helpers)
    start_date = request.form.get("start_date")
    print("START DATE: ",start_date)
    end_date = request.form.get("end_date")
    print("END DATE: ",end_date)

    file = request.files.get("images")
    image = file.read()
    # print("IMAGE_URL: ", image)
    # Security & Validation

    # We get the id from the session which is set when the user logs in
    # new_job = Jobs(
    #     helpee_id=3,
    #     status="NA",  # Not Accepted as default
    #     job_title=title,
    #     job_description=description,
    #     short_title="",
    #     short_type="",
    # )

    # db.session.add(new_job)
    # db.session.commit()
    # job_data = Jobs.query.get_or_404(new_job.id)
    return "success"

@posts_blueprint.route("/create_job", methods=["POST"])
def create_job():
    title = request.form.get("title")
    print("TITLE: ",title)
    description = request.form.get("description")
    print("DESCRIPTION: ",description)
    area = request.form.get("area")
    file = request.files.get("images")
    image = file.read()
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
    return render_template("/posts/view_post.html", job_data=job_data)


@posts_blueprint.route("/edit_post", methods=["POST"])
def edit_post():
    updated_data = request.json["edit_data"]
    updated_title = updated_data[1]
    updated_description = updated_data[2]
    updated_area = updated_data[3]

    updated_job = Jobs.query.filter_by(id=updated_data[0]).first()
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
