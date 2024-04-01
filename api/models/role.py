# Create and initiate database here. 
from api import db
from datetime import datetime

# Columns for the database below
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.role
        }