from flask import Blueprint, render_template, request,jsonify
from db.modals import Projects, Communities, Jobs
profile_blueprint = Blueprint("profile", __name__, template_folder="templates")


@profile_blueprint.route("/community_profile/<community_name>")
def community_profile_page(community_name):
    revert_format = community_name.replace("_", " ").title()
    community_data = Communities.query.filter_by(name=revert_format).first_or_404()
    community_id = community_data.id
    project_data = Projects.query.where(Projects.community_id == community_id).all()
    all_job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == community_id).all()
    # specific_job_data = Jobs.query.join(Projects, Jobs.project_id == Projects.id).where(Projects.community_id == community_id).all()
    get_project_names = Projects.query.join(Jobs, Projects.id == Jobs.project_id).all()
    print("LENGTH: ",len(all_job_data))
    print("LENGTH: ",len(get_project_names))
    return render_template("/profile/community_profile.html", community = community_data, projects = project_data, jobs = all_job_data, project_names = get_project_names)

