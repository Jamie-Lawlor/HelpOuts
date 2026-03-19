from flask import Blueprint, render_template, request, jsonify, redirect, session
from flask_login import login_required
from db.database import db
from db.models import (
    Projects,
    Communities,
    Jobs,
    UserJobs,
    Users,
    JobRequests,
    CommunityRequests,
    Skills,
    UserSkills
)

profile_blueprint = Blueprint("profile", __name__, template_folder="templates")


@profile_blueprint.route("/community_profile/<community_name>")
@login_required
def community_profile_page(community_name):
    revert_format = community_name.replace("_", " ").title()
    community_data = Communities.query.filter_by(name=revert_format).first_or_404()
    community_id = community_data.id
    project_data = Projects.query.where(Projects.community_id == community_id).all()
    all_job_data = (
        Jobs.query.join(Projects, Jobs.project_id == Projects.id)
        .where(Projects.community_id == community_id)
        .all()
    )
    # specific_job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == community_id).all()
    get_project_names = Projects.query.join(Jobs, Projects.id == Jobs.project_id).all()
    if session["type"] != "chairperson":
        user_data = Users.query.get_or_404(session["user_id"])
        return render_template(
            "/profile/community_profile.html",
            community=community_data,
            projects=project_data,
            jobs=all_job_data,
            project_names=get_project_names,
            user_data=user_data,
        )
    else:
        return render_template(
            "/profile/community_profile.html",
            community=community_data,
            projects=project_data,
            jobs=all_job_data,
            project_names=get_project_names,
            user_data=None,
        )


@profile_blueprint.route("/helper_profile/<user_name>")
@login_required
def helper_profile_page(user_name):
    revert_format = user_name.replace("_", " ").title()
    user_data = Users.query.filter_by(name=revert_format).first_or_404()
    skills_data = Skills.query.all()
    user_skills = (
            Skills.query.join(UserSkills, Skills.id == UserSkills.skill_id)
            .where(UserSkills.user_id == user_data.id)
            .all()
        )
    # print(skills_data[26].skill)
    role = session["type"]
    print("ROLE: ", role)
    print("ROLE TYPE: ", type(role))
    if user_data.community_id is not None:
        community_id = user_data.community_id
        joined_community_data = Communities.query.get_or_404(community_id)
        all_job_data = (
            Jobs.query.join(UserJobs, Jobs.id == UserJobs.job_id)
            .where(UserJobs.user_id == user_data.id)
            .all()
        )
        print(all_job_data)
        print(skills_data)
        return render_template(
            "/profile/helper_profile.html",
            user_data=user_data,
            community_data=joined_community_data,
            user_jobs=all_job_data,
            skills = skills_data,
            user_skills = user_skills,
            role=role,
        )
    else:
        return render_template(
            "/profile/helper_profile.html",
            user_data=user_data,
            skills = skills_data,
            community_data=None,
            user_jobs=None,
        )


@profile_blueprint.route("/community_settings/<community_name>")
@login_required
def settings_page(community_name):
    if session["type"] != "chairperson":
        return redirect("/home_page/")
    else:
        revert_format = community_name.replace("_", " ").title()
        community_data = Communities.query.filter_by(name=revert_format).first_or_404()
        community_id = community_data.id
        project_data = Projects.query.where(Projects.community_id == community_id).all()
        all_job_data = (
            Jobs.query.join(Projects, Jobs.project_id == Projects.id)
            .where(Projects.community_id == community_id)
            .all()
        )
        # specific_job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == community_id).all()
        get_project_names = Projects.query.join(
            Jobs, Projects.id == Jobs.project_id
        ).all()
        return render_template(
            "/community_settings.html",
            community=community_data,
            projects=project_data,
            jobs=all_job_data,
            project_names=get_project_names,
        )


@profile_blueprint.route("/helper_settings/<user_name>")
@login_required
def helper_settings_page(user_name):
    if session["type"] != "helper":
        return redirect("/home_page/")
    else:
        revert_format = user_name.replace("_", " ").title()
        helper_data = Users.query.filter_by(name=revert_format).first_or_404()

        return render_template(
            "/helper_settings.html",
            helper=helper_data,
        )


@profile_blueprint.route("/requests/<community_name>")
@login_required
def community_requests_page(community_name):
    revert_format = community_name.replace("_", " ").title()
    community_data = Communities.query.filter_by(name=revert_format).first_or_404()
    community_id = community_data.id
    job_requests = (
        JobRequests.query.join(Jobs, JobRequests.job_id == Jobs.id)
        .join(Users, JobRequests.user_id == Users.id)
        .where(Users.community_id == community_id, JobRequests.status == "P")
        .all()
    )
    community_requests = (
        CommunityRequests.query.join(
            Communities, CommunityRequests.community_id == Communities.id
        )
        .join(Users, CommunityRequests.user_id == Users.id)
        .where(CommunityRequests.status == "P")
        .all()
    )
    job_list = []
    user_list = []
    community_request_list = []
    for request in job_requests:
        job_list.append(Jobs.query.get_or_404(request.job_id))
        user_list.append(Users.query.get_or_404(request.user_id))

    for user in community_requests:
        community_request_list.append(Users.query.get_or_404(user.user_id))

    return render_template(
        "/requests.html",
        community=community_data,
        job_list=job_list,
        user_list=user_list,
        community_request_list=community_request_list,
    )


@profile_blueprint.route("/accept_helper_job_request", methods=["POST"])
def accept_helper_job():
    data = request.json["data"]
    job_id = data[0]
    updated_job_request = JobRequests.query.where(JobRequests.job_id == job_id).first()
    updated_job_request.status = "A"
    updated_job_request.confirmed_date = db.func.current_timestamp()
    check_helper = Users.query.where(Users.id == updated_job_request.user_id).first()
    job_accepted = UserJobs(user_id=check_helper.id, job_id=job_id)
    db.session.add(job_accepted)
    db.session.commit()
    return ""


@profile_blueprint.route("/request_join_community", methods=["POST"])
def join_community():
    data = request.json["data"]
    community_id = data[0]
    helper_id = session["user_id"]
    pending_request = CommunityRequests(
        user_id=helper_id,
        community_id=community_id,
        created_date=db.func.current_timestamp(),
    )
    db.session.add(pending_request)
    db.session.commit()
    return ""


@profile_blueprint.route("/accept_join_community", methods=["POST"])
def accept_join_community():
    data = request.json["data"]
    helper_id = data[0]
    status = data[1]

    accept_user = CommunityRequests.query.where(
        CommunityRequests.user_id == helper_id
    ).first()
    accept_user.status = status
    accept_user.confirmed_date = db.func.current_timestamp()
    if status == "A":
        check_helper = Users.query.where(Users.id == accept_user.user_id).first()
        check_helper.community_id = accept_user.community_id
    db.session.commit()
    return ""
