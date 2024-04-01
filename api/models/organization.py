from api import db
from datetime import datetime

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    location = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    partner = db.relationship('Partner', backref=db.backref('organizations', lazy=True))


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "partner_id": self.partner_id,
            "date_created": self.date_created
        }