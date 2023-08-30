from api import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    students = db.relationship('Student', backref='site')
    cohorts = db.relationship('Cohort', backref='site')
    admins = db.relationship('Admin', backref='site')