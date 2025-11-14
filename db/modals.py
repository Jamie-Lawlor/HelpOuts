from db.database import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    