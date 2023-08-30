# Create and initiate database here. 
from api import db
from datetime import datetime

# Columns for the database below
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    students = db.relationship('Student', backref='attendance')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def serialize(self):
        return {
            "id": self.id, 
            "admin_id": self.admin_id, 
            "cohort_id": self.cohort_id, 
            "students": self.students, 
            "date_created": self.date_created
        }