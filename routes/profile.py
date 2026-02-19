from flask import Blueprint, render_template, request, jsonify
from db.models import Projects, Communities, Jobs, UserJobs, Users

profile_blueprint = Blueprint("profile", __name__, template_folder="templates")


@profile_blueprint.route("/community_profile/<community_name>")
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
    return render_template(
        "/profile/community_profile.html",
        community=community_data,
        projects=project_data,
        jobs=all_job_data,
        project_names=get_project_names,
    )


@profile_blueprint.route("/helper_profile/<user_name>")
def helper_profile_page(user_name):
    revert_format = user_name.replace("_", " ").title()
    user_data = Users.query.filter_by(name=revert_format).first_or_404()
    print(user_data.name)
    community_id = user_data.community_id
    joined_community_data = Communities.query.get_or_404(community_id)
    all_job_data = (
        Jobs.query.join(UserJobs, Jobs.id == UserJobs.job_id)
        .where(UserJobs.user_id == user_data.id)
        .all()
    )
    print(all_job_data)
    return render_template(
        "/profile/helper_profile.html",
        user_data=user_data,
        community_data=joined_community_data,
        user_jobs=all_job_data,
    )


@profile_blueprint.route("/community_settings/<community_name>")
def settings_page(community_name):
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
    return render_template(
        "/community_settings.html",
        community=community_data,
        projects=project_data,
        jobs=all_job_data,
        project_names=get_project_names,
    )


@profile_blueprint.route("/helper_settings/<user_name>")
def helper_settings_page(user_name):
    revert_format = user_name.replace("_", " ").title()
    helper_data = Users.query.filter_by(name=revert_format).first_or_404()

    return render_template(
        "/helper_settings.html",
        helper=helper_data,
    )
