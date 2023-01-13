# Create and initiate database here. 
from app import Portal 
from datetime import datetime 
app = Portal()
db = app.db

# Columns for the database below
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False) # should this be an option
    company_id = db.Column(db.Integer, nullable=False) # figure out if this should be a real object
    date_created = db.Column(db.DateTime, default=datetime.utcnow)