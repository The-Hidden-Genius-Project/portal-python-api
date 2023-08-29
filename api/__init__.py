from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def Initialize_Portal(): 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY_YA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from api.models.user import User
    from api.models.job import Job
    from api.models.organization import Organization
    from api.models.application import Application
    
    create_database(app)

    return app, db

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        app.app_context().push()
        db.create_all()
        print('Created Database!')



# https://github.com/techwithtim/Flask-Web-App-Tutorial/blob/main/website/__init__.py 
# Look at this link to fix this issue.  