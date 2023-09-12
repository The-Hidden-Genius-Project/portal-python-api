from api import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    attendances = db.relationship('Attendance', backref='student')


    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "cohort_id": self.cohort_id
        }