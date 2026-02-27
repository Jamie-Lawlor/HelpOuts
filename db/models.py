from db.database import db
from sqlalchemy.orm import validates
from datetime import datetime
import re

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column( db.String(6), nullable=False, default="guest")  # can be 'helpee' or 'helper'
    work_area = db.Column(db.String(100), nullable=True)
    specialism = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    private_key = db.Column(db.LargeBinary, nullable = True)
    public_key = db.Column(db.LargeBinary, nullable = True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=True)
    profile_picture = db.Column(db.String(1000), nullable = True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_accuracy = db.Column(db.Numeric(5,2), nullable=True)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty")
        if '@' not in email:
            raise ValueError("Invalid email address, must contain '@'")
        return email
    
   
    @validates('password')
    def validate_password(self, key, password): # 8 characters, 1 capital, 1 lower, 1 number, 1 special
        valid_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
        if not password:
            raise ValueError("Password cannot be empty")
        if not re.match(valid_pattern, password):
            raise ValueError("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character")
        return password
    
    @validates('type')
    def validate_type(self, key, type):
        if not type:
            raise ValueError("Type cannot be empty")
        if type not in ['chairperson', 'helper']:
            raise ValueError("Type must be either 'chairperson' or 'helper'")
        return type
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserPermissions(db.Model):
    __tablename__ = 'user_permissions'
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
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    @validates('star_rating')
    def validate_star_rating(self, key, star_rating):
        if not star_rating:
            raise ValueError("Star rating cannot be empty")
        if not (1 <= star_rating <= 5):
            raise ValueError("Star rating must be between 1 and 5")
        return star_rating
    
    @validates('review')
    def validate_review(self, key, review):
        if not review:
            raise ValueError("Review cannot be empty")
        if len(review) > 500:
            raise ValueError("Review cannot exceed 500 characters")
        return review
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.LargeBinary, nullable =False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Message content cannot be empty")
        if len(content) > 1000:
            raise ValueError("Message content cannot exceed 1000 characters")
        return content
    
    @validates('timestamp')
    def validate_timestamp(self, key, timestamp):
        if not timestamp:
            raise ValueError("Timestamp cannot be empty")
        return timestamp
    
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    status = db.Column(db.String(3), nullable=False, default="D")
    area = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    short_title = db.Column(db.String(50), nullable=True)
    short_type = db.Column(db.String(20), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if not start_date:
            return None
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if self.end_date and start_date > self.end_date:
            raise ValueError("Start date cannot be after end date")
        if start_date.date() < datetime.now().date():
            raise ValueError("Start date cannot be in the past")
        return start_date

    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if not end_date:
            return None
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if self.start_date and end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        return end_date
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserJobs(db.Model):
    __tablename__ = 'user_jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    
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
    profile_picture = db.Column(db.String(1000), nullable =True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_title = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.String(1000), nullable=False)
    project_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(3), nullable=False, default="D")
    number_of_helpers = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    community_id = db.Column(db.Integer,db.ForeignKey("communities.id"), nullable=False)
    
    
    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if not start_date:
            return None
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if self.end_date and start_date > self.end_date:
            raise ValueError("Start date cannot be after end date")
        if start_date.date() < datetime.now().date():
            raise ValueError("Start date cannot be in the past")
        return start_date

    
    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if not end_date:
            return None
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if self.start_date and end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        return end_date

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_json = db.Column(db.String(1000), nullable = False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

