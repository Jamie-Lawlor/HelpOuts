from flask import Blueprint, render_template, request, redirect, session, jsonify
from db.database import db
from db.modals import Projects, Jobs, ProjectJobs, CommunityProjects

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
    project_type_selected = request.form.get("type")
    print("TYPE: ",project_type_selected)
    helpers = request.form.get("helpers")
    print("HELPERS: ",helpers)
    start_date_selected = request.form.get("start_date")
    print("START DATE: ",start_date_selected)
    end_date_selected = request.form.get("end_date")
    print("END DATE: ",end_date_selected)
    file = request.files.get("images")
    # print("IMAGE_URL: ", image)
    # Security & Validation

    new_project = Projects(
        # HARDCODED
        community_id=1,
        project_title=title,  # Not Accepted as default
        project_description=description,
        project_type=project_type_selected,
        number_of_helpers=helpers,
        start_date = start_date_selected,
        end_date = end_date_selected
    )
    db.session.add(new_project)
    db.session.commit()
    new_project_link = CommunityProjects(
        # HARDCODED
        community_id=1,
        project_id = new_project.id
    )
    db.session.add(new_project_link)
    db.session.commit()
    new_project_data = Projects.query.get_or_404(new_project.id)
    return jsonify(new_project_data.to_dict())

@posts_blueprint.route("/create_job", methods=["POST"])
def create_job():
    title = request.form.get("title")
    print("TITLE: ",title)
    description = request.form.get("description")
    print("DESCRIPTION: ",description)
    area = request.form.get("area")
    file = request.files.get("images")

    # Security & Validation 

    # We get the id from the session which is set when the user logs in
    new_job = Jobs(
        #HARDCODED
        helper_id = 1,
        helpee_id=2,
        project_id = 1,
        status="NA", # Not Accepted as default
        area=area,
        job_title=title,
        job_description=description,
        short_title="",
        short_type="",
    )
    db.session.add(new_job)
    db.session.commit()
    new_job_for_project = ProjectJobs(
        #HARDCODED
        project_id = 1,
        job_id = new_job.id
    )
    db.session.add(new_job_for_project)
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

@posts_blueprint.route("/job_accepted", methods =["POST"])
def job_accepted():
    data = request.json["data"]
    job_id = data[0]
    helper_id = data[1]
    updated_post = Jobs.query.filter_by(id=job_id).first()
    updated_post.helper_id = helper_id
    db.session.commit()
    return ""