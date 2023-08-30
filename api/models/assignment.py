from api import db 

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    github = db.Column(db.String)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))


    def serialize(self):
        return {
            "id": self.id, 
            "title": self.title, 
            "github": self.github, 
            "cohort_id": self.cohort_id
        }