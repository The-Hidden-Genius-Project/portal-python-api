from api import db

class Stipend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
