from api import db

class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)


    def serialize(self):
        return {
            "id": self.id, 
            "amount": self.amount, 
            "students": self.students
        }
