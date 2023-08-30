from api import db

class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    students = db.relationship('Student', backref='bonus')


    def serialize(self):
        return {
            "id": self.id, 
            "amount": self.amount, 
            "students": self.students
        }
