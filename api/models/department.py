from api import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    admins = db.relationship("Admin", backref='department')

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "admins": self.admins
        }