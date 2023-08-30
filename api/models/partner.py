from api import db

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    company = db.Column(db.String)
    position = db.Column(db.String)
    jobs = db.relationship('Job', backref="partner")


    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "company": self.company, 
            "position": self.position, 
            "jobs": self.jobs
        }

