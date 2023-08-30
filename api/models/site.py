from api import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)

    def serialize(self):
        return {
            "id": self.id, 
            "location": self.location
        }