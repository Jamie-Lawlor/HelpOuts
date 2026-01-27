from flask import Blueprint, render_template, request, redirect, session, jsonify
from db.database import db
from db.models import Projects, Jobs, Users, Subscriptions
import os
import json
import magic
from pywebpush import webpush, WebPushException

Allowed_File_Types = {"image/png", "image/jpeg", "image/jpg"}

posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/add_project/")
def project_page():
    return render_template("/posts/add_project.html")

@posts_blueprint.route("/add_job/")
def post_page():
    # ASSUMING WE ARE DUNDALK TIDY TOWNS COMMUNITY ADMIN
    project_data = Projects.query.where(Projects.community_id == 1).all()

    return render_template("/posts/add_job.html", projects = project_data)

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
    if(request.files.get("images") is not None):
        file = request.files.get("images")
        # print("IMAGE_URL: ", image)

        # Security & Validation
        if not image_validation(file):
            print("Invalid File")
        elif image_validation(file):
            print("Valid File")
    

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
    new_project_data = Projects.query.get_or_404(new_project.id)
    return jsonify(new_project_data.to_dict())

@posts_blueprint.route("/create_job", methods=["POST"])
def create_job():
    project_id = request.form.get("project_id")
    title = request.form.get("title")
    print("TITLE: ",title)
    description = request.form.get("description")
    print("DESCRIPTION: ",description)
    area = request.form.get("area")
    type = request.form.get("type")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    if(request.files.get("images") is not None):
        file = request.files.get("images")
        # print("IMAGE_URL: ", image)

        # Security & Validation
        if not image_validation(file):
            print("Invalid File")
        elif image_validation(file):
            print("Valid File")

    # We get the id from the session which is set when the user logs in
    new_job = Jobs(
        #HARDCODED
        helper_id = 2,
        helpee_id=2,
        project_id = project_id,
        status="NA", # Not Accepted as default
        area=area,
        job_title=title,
        job_description=description,
        short_title="",
        short_type=type,
        created_date = db.func.current_timestamp(),
        start_date = start_date,
        end_date = end_date
    )
    db.session.add(new_job)
    db.session.commit()
    job_data = Jobs.query.get_or_404(new_job.id)
    return jsonify(job_data.to_dict())

@posts_blueprint.route("/view_post/<post_title>")
def view_specific_post_page(post_title):
    revert_format = post_title.replace("_", " ").title()
    vapid_key = os.getenv("VAPID_PUBLIC_KEY_BASE_64")
    job_data = Jobs.query.filter_by(job_title=revert_format).first_or_404().to_dict()
    return render_template("/posts/view_post.html", job_data=job_data, vapid_key = vapid_key)


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
    return updated_job.job_title


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

@posts_blueprint.route("/send_job_accepted_notification", methods = ["POST"])
def send_notification():
    data = request.json["data"]
    job_id = data[0]
    helper_id = data[1]
    user_data = Users.query.get_or_404(helper_id)
    job_accepted = Jobs.query.get_or_404(job_id)
    subscriptions = Subscriptions.query.all()
    results = trigger_push_notifications_for_admin(subscriptions, "HelpOuts", f"{user_data.name} has accepted job: \"{job_accepted.job_title}\"")
    print("USERID: ",job_accepted.job_title)
    return ""

def trigger_push_notifications_for_admin(subscriptions, title, body):
    return [trigger_push_notification(subscription, title, body)
            for subscription in subscriptions]

def trigger_push_notification(push_subscription, title, body):
    try:
        response = webpush(
            subscription_info=json.loads(push_subscription.subscription_json),
            data=json.dumps({"title": title, "body": body}),
            vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
            vapid_claims={
                "sub": os.getenv("VAPID_CLAIM_EMAIL")
            }
        )
        return response.ok
    except WebPushException as ex:
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  )
        return False

def image_validation(file):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file)
    file_path, file_extension = os.path.splitext(file)

    if mime_type in Allowed_File_Types and (file_extension.lower() == ".png" or file_extension.lower() == ".jpeg" or file_extension.lower() == ".jpg"):
        return True
    elif mime_type not in Allowed_File_Types:
        print("File type is not an image")
        return False
    elif file_extension.lower() != ".png":
        print("File extension is not a .png, must be .jpg, .jpeg or .png")
        return False
    elif file_extension.lower() != ".jpeg":
        print("File extension is not a .jpeg, must be .jpg, .jpeg or .png")
        return False
    elif file_extension.lower() != ".jpg":
        print("File extension is not a .jpg, must be .jpg, .jpeg or .png")
        return False
    return False
