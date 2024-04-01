# Create and initiate database here. 
from api import db
from datetime import datetime

# Columns for the database below
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String)    
    email = db.Column(db.String)
    name = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def serialize(self):
        return {
            "id": self.id,
            "google_id": self.google_id,
            "email": self.email,
            "name": self.name, 
            "role_id": self.role_id,
            "date_created": self.date_created,
        }