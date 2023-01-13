from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

class Portal(): 
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY_YA'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)



