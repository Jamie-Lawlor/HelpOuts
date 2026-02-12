from flask import Blueprint, render_template, request, redirect
from db.database import db

api_blueprint = Blueprint("api", __name__, template_folder="templates")


@api_blueprint.route("/test")
def test():
    return "if you can see this, yayyy"