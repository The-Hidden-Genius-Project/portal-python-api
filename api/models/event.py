from api import db 
import json
from json import JSONEncoder
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'site_id': self.site_id, 
            'date_created': date_created
        }
