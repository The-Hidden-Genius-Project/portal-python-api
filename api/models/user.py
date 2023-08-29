from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(150), unique=True) 
    email = db.Column(db.String(150))
    name = db.Column(db.String(140))
    role = db.Column(db.String(140), default="User")


    def serialize(self):
        return {
            "id": self.id,
            "google_id": self.google_id,
            "email": self.email, 
            "name": self.name,
            "role": self.role
        }