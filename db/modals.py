from db.database import db
from werkzeug.security import generate_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column( db.String(6), nullable=False, default="helpee")  # can bee 'helpee' or 'helper'
    work_area = db.Column(db.String(100), nullable=True)
    specialism = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    private_key = db.Column(db.String(1000), nullable =False)
    public_key = db.Column(db.String(1000), nullable =False)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=True)
    profile_picture = db.Column(db.String(1000), nullable =False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserPermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    accepted_terms = db.Column(db.Boolean, nullable=False, default=False)
    accepted_gdpr = db.Column(db.Boolean, nullable=False, default=False)
    accepted_health_safety = db.Column(db.Boolean, nullable=False, default=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    helper_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    star_rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    aes_key = db.Column(db.String(1000), nullable =False)
    iv = db.Column(db.String(1000), nullable =False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    helper_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    helpee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    status = db.Column(db.String(3), nullable=False, default="D")
    area = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    short_title = db.Column(db.String(50), nullable=True)
    short_type = db.Column(db.String(20), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MapIcon(db.Model):
    __tablename__ = 'map_icons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    icon_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class JobLocation(db.Model):
    __tablename__ = 'job_location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    icon_id = db.Column(db.Integer, db.ForeignKey("map_icons.id"), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    
class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    profile_picture = db.Column(db.String(1000), nullable =False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer,db.ForeignKey("communities.id"), nullable=False)
    project_title = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.String(1000), nullable=False)
    project_type = db.Column(db.String(20), nullable=False)
    number_of_helpers = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
    
# Joiner table used to hold which jobs are linked to which project
class ProjectJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
# Joiner table user to hold what projects a community has ongoing
class CommunityProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_json = db.Column(db.String(1000), nullable = False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}