from api import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "user_id": self.user_id, 
            "date_created": self.date_created
        }