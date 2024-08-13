# Import API and initiate database here. 
from api import db
from datetime import datetime

# Attendance columns for the database below
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String)
    event_id = db.Column(db.String)
    event = db.relationship('Event', backref=db.backref('attendances', lazy=True))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Serialize data into JSON
    def serialize(self):
        return {
            "id": self.id, 
            "admin_id": self.admin_id, 
            "cohort_id": self.cohort_id, 
            "event_id": self.event_id,
            "student_id": self.student_id, 
            "notes": self.notes,
            "date_created": self.date_created
        }