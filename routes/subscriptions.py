from flask import Blueprint, render_template, request, redirect, session, jsonify
from db.database import db
from db.models import Subscriptions

subscriptions_blueprint = Blueprint("subscriptions", __name__, template_folder="templates")


@subscriptions_blueprint.route("/api/push-subscriptions", methods=["POST"])
def create_push_subscription():
    json_data = request.get_json()
    # Checks if subscription exists
    subscription = Subscriptions.query.filter_by(
        subscription_json=json_data['subscription_json']
    ).first()
    if subscription is None:
        subscription = Subscriptions(
            subscription_json=json_data['subscription_json']
        )
        db.session.add(subscription)
        db.session.commit()
    return jsonify({
        "status": "success"
    })