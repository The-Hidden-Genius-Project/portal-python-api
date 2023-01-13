# Create and initiate database here. 
from app import Portal 
from datetime import datetime 
app = Portal()
db = app.db

# Columns for the database below
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)