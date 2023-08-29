# Imported libraries
import json
import os
import pathlib
import requests
from api import Initialize_Portal
from flask import Flask, session, abort, redirect, request, render_template, Response
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from api.models.user import User
from api.models.job import Job
from api.models.organization import Organization
from api.models.application import Application
from flask import jsonify

# Initiate the app w/ Flask
app, db = Initialize_Portal()

# This is the line that we use to test localhost, remove in production. 
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "371018060880-7pf78bv430u3erbcujo11gpu7qlgjfm2.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# Function authenticates access to the platform. 
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper


# Validate email domain 
def validate_email_domain(email): 
    words = email.split("@")
    if ("hgs" in words):
        return words[2] == "hiddengeniusproject.org"
    else: 
        return words[1] == "hiddengeniusproject.org"

# This function will create the state to receive and response from the google api. 
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# This function returns data back to us after user confirmations.
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info['sub']
    session["name"] = id_info['name']
    session["email"] = id_info['email']


    # creating user if not existing. 
    user = User(email=session["email"], google_id=session["google_id"])

    print(User.query.all())

    # check if user email is valid
    return redirect("/dashboard")



# This email just clears the session, removing user. 
@app.route("/logout") 
def logout():
    session.clear()
    return redirect("/")

# Dashboard returned to use when we have all the things we need. 
@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"





# Jobs serialized into JSON data
@app.route('/jobs', methods=['GET'])
def jobs():
    jobs = Job.query.all()
    serialzied = [j.serialize() for j in jobs]
    return serialzied, 200

# new Jobs
@app.route("/jobs/new", methods=['POST'])
def new_job():
    if request.method == 'POST':
        job_title = request.args.get('title')
        job_description = request.args.get('description')
        job_type = request.args.get('type')
        job_organization_id = request.args.get('organization_id')
        new_job = Job(
            title=job_title, 
            description=job_description, 
            type=job_type, 
            organization_id=job_organization_id
        )

        try: 
            db.session.add(new_job)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401
        
# GET specific job page
@app.route('/jobs/<id>', methods=['GET'])
def show_job(id):
    return Job.query.get(id).serialize(), 200


# ORGANIZATIONS routes
@app.route('/organizations', methods=['GET'])
def organizations():
    organizations = Organization.query.all()
    serialzied = [o.serialize() for o in organizations]
    return serialzied, 200


@app.route('/new_organization', methods=['POST'])
def new_organization():
    if request.method == 'POST':
        org_name = request.args.get('name')
        org_location = request.args.get('location')
        org_admin = request.args.get('user_id')
        new_organization = Organization(
            name=org_name, 
            location=org_location, 
            user_id=org_admin   
        )

        try: 
            db.session.add(new_organization)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401
        

# GET specific organization page
@app.route('/organizations/<id>', methods=['GET'])
def show_organization(id):
    return Organization.query.get(id).serialize(), 200


# APPLICATIONS route
@app.route('/jobs/<id>/applications', methods=['GET'])
def applications(id):
    apps = Application.query.filter_by(job_id = id)
    serialzied = [a.serialize() for a in apps]
    return serialzied, 200

@app.route('/jobs/<id>/applications/new', methods=['POST'])
def new_application(id):
    if request.method == 'POST':
        job_id = id
        user_id = request.args.get('user_id')
        new_application = Application(
            user_id=user_id, 
            job_id=job_id
        )

        try: 
            db.session.add(new_application)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401

# USERS routes
@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    serialzied = [u.serialize() for u in users]
    return serialzied, 200

@app.route('/users/new', methods=['POST'])
def new_user():
    if request.method == 'POST':
        user_google_id = request.args.get('google_id')
        user_email = request.args.get('email')
        user_name = request.args.get('name')
        user_role = request.args.get('role')
        new_user= User(
            google_id=user_google_id, 
            email=user_email, 
            name=user_name, 
            role=user_role   
        )

        try: 
            db.session.add(new_user)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401



# api page
@app.route('/api')
def api():
    return render_template('api.html')

# Run the app. 
if __name__ == "__main__":
    app.run(debug=True)