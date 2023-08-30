from api import db 

class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    students = db.relationship('Student', backref='attendance')
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "students": self.students,
            "site_id": self.site_id
        }