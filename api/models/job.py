# Create and initiate database here. 
from api import db
from datetime import datetime

# Columns for the database below
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False) # should this be an option # figure out if this should be a real object
    date_created = db.Column(db.DateTime, default=datetime.utcnow)