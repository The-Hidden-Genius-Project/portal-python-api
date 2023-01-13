from flask import Flask, session, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask("Google Login Ap")
app.secret_key = "geniuslabs"

@app.route('/login')
def login():
    def wrapper(*args, **kwargs):
        if "google_id" not in session: 
            return abort(401)
        else: 
            
@app.route('/callback')
def callback():

@app.route('/logout')
def logout():


@app.route('/')
def index():
    return "Hello World"

@app.route('/protected_area')
def protected_area():
    return "protected"


if __name__ == "__main__": 
    app.run(debug=True)




class Portal(): 
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY_YA'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

