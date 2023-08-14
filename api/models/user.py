from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(150), unique=True) 
    email = db.Column(db.String(150))