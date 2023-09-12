from api import db 

class ApiKey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)


    def serialize(self):
        return {
            "id": self.id,
            "hash": self.hash
        }