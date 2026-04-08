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
    UserSkills,
    Logs,
)

profile_blueprint = Blueprint("profile", __name__, template_folder="templates")


@profile_blueprint.route("/community_profile/<community_name>")
@login_required
def community_profile_page(community_name):
    revert_format = community_name.replace("_", " ").title()
    community_data = Communities.query.filter_by(name=revert_format).first_or_404()
    community_id = community_data.id
    role = session["type"]
    project_data = Projects.query.where(Projects.community_id == community_id).all()
    all_job_data = (
        Jobs.query.join(Projects, Jobs.project_id == Projects.id)
        .where(Projects.community_id == community_id)
        .all()
    )
    # specific_job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == community_id).all()
    get_project_names = Projects.query.join(Jobs, Projects.id == Jobs.project_id).all()
    usersList = Users.query.where(
        Users.community_id == community_id, Users.type == "helper"
    ).all()
    print(usersList)
    logs = Logs(
        user_id=session["user_id"],
        action=f"Viewed - {community_name}",
        target="Communities",
    )
    db.session.add(logs)
    db.session.commit()
    if session["type"] != "chairperson":
        user_data = Users.query.get_or_404(session["user_id"])
        return render_template(
            "/profile/community_profile.html",
            community=community_data,
            projects=project_data,
            jobs=all_job_data,
            project_names=get_project_names,
            usersList=usersList,
            user_data=user_data,
        )
    else:
        return render_template(
            "/profile/community_profile.html",
            community=community_data,
            projects=project_data,
            jobs=all_job_data,
            project_names=get_project_names,
            usersList=usersList,
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
    print(user_skills)
    if user_data.experience is not None:
        user_experience = user_data.experience.split(",")
        print(user_experience)
    else:
        user_experience = ""

    logs = Logs(
        user_id=session["user_id"], action=f"Viewed - {user_name}", target="Profile"
    )
    db.session.add(logs)
    db.session.commit()

    if user_data.community_id is not None:
        role = session["type"]
        community_id = user_data.community_id
        joined_community_data = Communities.query.get_or_404(community_id)
        all_job_data = (
            Jobs.query.join(UserJobs, Jobs.id == UserJobs.job_id)
            .where(UserJobs.user_id == user_data.id)
            .all()
        )

        return render_template(
            "/profile/helper_profile.html",
            user_data=user_data,
            community_data=joined_community_data,
            user_jobs=all_job_data,
            skills=skills_data,
            user_skills=user_skills,
            user_experience=user_experience,
            role=role,
        )
    else:
        return render_template(
            "/profile/helper_profile.html",
            user_data=user_data,
            skills=skills_data,
            community_data=None,
            user_jobs=None,
            user_skills=user_skills,
            user_experience=user_experience,
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
        .where(
            CommunityRequests.status == "P",
            CommunityRequests.community_id == community_id,
        )
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
    job_id = request.json["data"]
    updated_job_request = JobRequests.query.where(JobRequests.job_id == job_id).first()
    updated_job_request.status = "A"
    updated_job_request.confirmed_date = db.func.current_timestamp()
    check_helper = Users.query.where(Users.id == updated_job_request.user_id).first()
    job_accepted = UserJobs(user_id=check_helper.id, job_id=job_id)
    logs = Logs(
        user_id=session["user_id"], action=f"Accepted - {job_id}", target="Jobs"
    )
    db.session.add(logs)
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
    logs = Logs(
        user_id=session["user_id"],
        action=f"Join Request - {community_id}",
        target="Communities",
    )
    db.session.add(logs)
    db.session.add(pending_request)
    db.session.commit()
    return ""


@profile_blueprint.route("/accept_join_community", methods=["POST"])
def accept_join_community():
    data = request.json["data"]
    helper_id = data[0]
    status = data[1]
    print("HELPER ID: ", id)
    print("STATUS: ", status)
    accept_user = CommunityRequests.query.where(
        CommunityRequests.user_id == helper_id
    ).first()
    accept_user.status = status
    accept_user.confirmed_date = db.func.current_timestamp()
    if status == "A":
        check_helper = Users.query.where(Users.id == accept_user.user_id).first()
        check_helper.community_id = accept_user.community_id

    logs = Logs(
        user_id=session["user_id"],
        action=f"Accepted Request - {helper_id}",
        target="Communities",
    )
    db.session.add(logs)
    db.session.commit()
    return ""


@profile_blueprint.route("/remove_skill", methods=["POST"])
def remove_skill():
    if session["type"] != "helper":
        return ""
    else:
        skill_data = request.json["data"]
        skill_to_be_removed = (
            UserSkills.query.join(Users, UserSkills.user_id == Users.id)
            .join(Skills, UserSkills.skill_id == Skills.id)
            .where(UserSkills.user_id == session["user_id"], Skills.skill == skill_data)
            .first_or_404()
        )
        db.session.delete(skill_to_be_removed)
        db.session.commit()
        return ""


@profile_blueprint.route("/update_helper_profile", methods=["POST"])
def update_helper_profile():
    # if session["type"] != "helper":
    #     return ""
    # else:
    updated_data = request.json["data"]
    updated_availability = updated_data[0]
    updated_skills = updated_data[1]
    updated_experience = updated_data[2].replace("\n", ",")
    print(updated_experience)

    update_user = Users.query.get_or_404(session["user_id"])
    if update_user.availability is not updated_availability:
        update_user.availability = updated_availability

    if updated_skills is not None or len(updated_skills) != 0:
        skills_list = Skills.query.all()
        skills_id_list = []
        for skill in skills_list:
            if skill.skill in updated_skills:
                skills_id_list.append(skill.id)

        for skill_id in skills_id_list:
            add_skills = UserSkills(user_id=session["user_id"], skill_id=skill_id)
            db.session.add(add_skills)

    if update_user.experience is None:
        update_user.experience = updated_experience

    elif update_user.experience is not updated_experience:
        update_user.experience = update_user.experience + "," + updated_experience

    if (
        updated_availability is None
        and updated_skills is None
        and updated_experience is None
    ):
        return ""
    else:
        logs = Logs(
            user_id=session["user_id"], action=f"Update Profile", target="Profile"
        )
        db.session.add(logs)
        db.session.commit()

    return ""
