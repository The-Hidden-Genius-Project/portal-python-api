from marshmallow import Schema, fields
from api import db 
import json
from json import JSONEncoder

class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'site_id': self.site_id
        }

