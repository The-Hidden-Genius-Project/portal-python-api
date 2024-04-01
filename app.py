# Imported libraries
import json
import os
import pathlib
import requests
from api import Initialize_Portal
from flask import Flask, session, abort, redirect, request, render_template, Response
from google.oauth2 import id_token
from binascii import hexlify
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError



###################################################################
# Models imported
from api.models.job import Job
from api.models.user import User
from api.models.role import Role
from api.models.organization import Organization
from api.models.application import Application
from api.models.admin import Admin
from api.models.assignment import Assignment
from api.models.cohort import Cohort
from api.models.department import Department
from api.models.partner import Partner
from api.models.site import Site
from api.models.student import Student
from api.models.bonus import Bonus
from api.models.stipend import Stipend
from api.models.attendance import Attendance


#### controllers ####

from api.controllers.users_controller import UsersController
from api.controllers.roles_controller import RolesController
###################################################################

# Initiate the app w/ Flask, DB
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


    print(session['google_id'])
    print(session['name'])
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



###########################################################################################################

# Post a new role for each user. 
@app.route("/roles/new", methods=['POST'])
def newRole():
    if request.method == 'POST':
        response = RolesController.newRole(
            request.args.get("name")
        )
        return response
    else: 
        return "something went wrong"
    
# Get all roles for each user
@app.route("/roles", methods=['GET'])
def roles():
    return RolesController.roles()


# Post a New User into the database
@app.route("/users/new", methods=['POST'])
def newUser():
    if request.method == 'POST':
        response = UsersController.newUser(
            request.args.get("google_id"),
            request.args.get("name"),
            request.args.get("email")
        )
        return response
    else: 
        return "something went wrong"


# Get all Users
@app.route("/users", methods=['GET'])
def users():
    return UsersController.users()

####################### Jobs Info #####################

@app.route('/jobs', methods=['GET'])
def jobs():
    jobs = Job.query.all()
    serialzied = [j.serialize() for j in jobs]
    return serialzied, 200


@app.route("/jobs/new", methods=['POST'])
def newJob():
    if request.method == 'POST':
        job_title = request.json['title']
        job_description = request.json['description']
        job_type = request.json['type']
        job_partner_id = request.json['partner_id']
        job_organization_id = request.json['organization_id']
        new_job = Job(
            title=job_title, 
            description=job_description, 
            type=job_type, 
            partner_id=job_partner_id, 
            organization_id=job_organization_id
        )
        print(new_job.description)
        print(new_job.description)
        try: 
            db.session.add(new_job)
            db.session.commit()

            return "", 204
        except SQLAlchemyError as e: 
            return "".format(e)
    return "", 200


@app.route('/jobs/<id>', methods=['GET'])
def showJob(id):
    return Job.query.get(id).serialize(), 200


####################### Organization Info #####################

@app.route('/organizations', methods=['GET'])
def organizations():
    organizations = Organization.query.all()
    serialzied = [o.serialize() for o in organizations]
    return serialzied, 200


@app.route('/organizations/new', methods=['POST'])
def newOrganization():
    if request.method == 'POST':
        org_name = request.args.get('name')
        org_location = request.args.get('location')
        org_admin = request.args.get('user_id')
        new_organization = Organization(
            name=org_name, 
            location=org_location, 
            partner_id=org_admin   
        )

        try: 
            db.session.add(new_organization)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401
        

# GET specific organization page
@app.route('/organizations/<id>', methods=['GET'])
def showOrganization(id):
    return Organization.query.get(id).serialize(), 200



####################### Applications Info #####################
@app.route('/jobs/<id>/applications/new', methods=['POST'])
def newApplication(id):
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

@app.route('/jobs/<id>/applications', methods=['GET'])
def applications(id):
    apps = Application.query.filter_by(job_id = id)
    serialzied = [a.serialize() for a in apps]
    return serialzied, 200


####################### Admin Info #####################
@app.route("/admins/new", methods=['POST'])
def newAdmin():
    if request.method == 'POST':
        name = request.args.get('name')
        email = request.args.get('email')
        department_id = request.args.get('department_id')
        site_id = request.args.get('site_id')
        new_admin = Admin(
            name=name, 
            email=email, 
            department_id=department_id,
            site_id=site_id
        )

        try: 
            db.session.add(new_admin)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401


@app.route('/admins', methods=['GET'])
def admins():
    admins = Admin.query.all()
    serialzied = [a.serialize() for a in admins]
    return serialzied, 200



####################### Site Info #####################
@app.route("/sites/new", methods=['POST'])
def new_site():
    if request.method == 'POST':
        site = request.args.get('location')
        new_site = Site(location=site)
        try: 
            db.session.add(new_site)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401



@app.route('/sites', methods=['GET'])
def sites():
    sites = Site.query.all()
    serialzied = [s.serialize() for s in sites]
    return serialzied, 200


################# Cohort Info  ######################
@app.route("/cohorts/new", methods=['POST'])
def newCohort():
    if request.method == 'POST':
        name = request.args.get('name')
        site_id = request.args.get('site_id')
        new_cohort = Cohort(name=name, site_id=site_id)
        try: 
            db.session.add(new_cohort)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401


@app.route('/cohorts/<id>', methods=['GET'])
def cohort(id):
    return Cohort.query.get(id).to_dict(), 200


@app.route('/cohorts', methods=['GET'])
def cohorts():
    cohorts = Cohort.query.all()
    serialzied = [c.serialize() for c in cohorts]
    return serialzied, 200


########################   Partner Info #########################

@app.route("/partners/new", methods=['POST'])
def newPartner():
    if request.method == 'POST':
        name = request.args.get('name')
        company = request.args.get('company')
        position = request.args.get('position')
        organization_id = request.args.get('organization_id')
        partner = Partner(name=name, company=company, position=position, organization_id=organization_id)
        try: 
            db.session.add(partner)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 401


@app.route('/partners', methods=['GET'])
def partners():
    partners = Partner.query.all()
    serialzied = [p.serialize() for p in partners]
    return serialzied, 200



######################### Attendance ###########################
@app.route("/cohorts/<id>/attendances/new", methods=['POST', 'GET'])
def newAttendance(id):
    if request.method == 'POST':
        admin_id = request.json['admin_id']
        cohort_id = id
        student_id = request.json['student_id']
        notes = request.json['notes']
       
        new_attendance = Attendance(notes=notes, admin_id=admin_id, cohort_id=cohort_id, student_id=student_id)
        
        try: 
            db.session.add(new_attendance)
            db.session.commit()
            return "", 204    
        except: 
            return "something happpend wrong"        
    return render_template('attendance.html', students=students)

@app.route('/cohorts/<id>/attendances', methods=['GET'])
def attendances(id):
    attendances = Attendance.query.filter_by(cohort_id = id)[::-1]
    serialzied = [a.serialize() for a in attendances]
    return serialzied, 200



######################### Students ###########################


@app.route('/cohorts/<id>/students', methods=['GET', 'POST'])
def students(id):
    students = Student.query.filter_by(cohort_id = id)[::-1]
    serialzied = [s.serialize() for s in students]
    return serialzied, 200


@app.route("/cohorts/<id>/students/new", methods=['POST'])
def newStudent(id):
    if request.method == 'POST':
        name = request.args.get('name')
        cohort_id = id
        new_student = Student(name=name, cohort_id=cohort_id)
        try: 
            db.session.add(new_student)
            db.session.commit()
            return "", 204
        except: 
            return "Something went wrong", 40



######################### APIKEY ###########################

@app.route('/api_key', methods=['POST'])
def ApiKey():
    key = hexlify(os.urandom(16))
    return key.decode(), 204


######################### APIKEY ###########################


# api page
@app.route('/api')
def api():
    return render_template('api.html')

# Run the app. 
if __name__ == "__main__":
    app.run(debug=True)
