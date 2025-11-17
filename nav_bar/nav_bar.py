from flask import Blueprint

navbar_blueprint = Blueprint(
    "nav_bar", __name__, static_folder="static", template_folder="templates"
)
