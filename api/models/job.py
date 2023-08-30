# Create and initiate database here. 
from api import db
from datetime import datetime

# Columns for the database below
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False) # should this be an option # figure out if this should be a real object
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "organation_id": self.organization_id,
            "date_created": self.date_created
        }