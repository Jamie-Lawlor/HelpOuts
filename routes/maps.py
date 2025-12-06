from flask import Blueprint, render_template

maps_blueprint = Blueprint("maps", __name__, template_folder="templates/maps")


@maps_blueprint.route("/maps/")
def inbox_page():
    return render_template("/maps/view_jobs.html")
