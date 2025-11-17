from db.database import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(
        db.String(3), nullable=False, default="helpee"
    )  # can bee 'helpee' or 'helper'
    work_area = db.Column(db.String(100), nullable=True)
    specialism = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Integer, nullable=True)


class UserPermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    accepted_terms = db.Column(db.Boolean, nullable=False, default=False)
    accepted_gdpr = db.Column(db.Boolean, nullable=False, default=False)
    accepted_health_safety = db.Column(db.Boolean, nullable=False, default=False)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    helper_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    star_rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=False)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    helper_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(3), nullable=False, default="D")
    area = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    short_title = db.Column(db.String(50), nullable=False)
    short_type = db.Column(db.String(20), nullable=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
