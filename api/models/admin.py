from api import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "email": self.email, 
            "department_id": self.department_id, 
            "site_id": self.site_id
        }