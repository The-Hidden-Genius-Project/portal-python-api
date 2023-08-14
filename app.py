# Imported libraries
import os
import pathlib
import requests
from api import Initialize_Portal
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from api.models.user import User
from api.models.attendance import Attendance


# Initiate the app w/ Flask
app = Initialize_Portal()

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

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    # creating user if not existing. 
    user = User(email=session["email"], google_id=session["google_id"])
    attendance = Attendance(user_id= user.id)

    print(User.query.all())

    # check if user email is valid
    return redirect("/protected_area")



# This email just clears the session, removing user. 
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Dashboard returned to use when we have all the things we need. 
@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

# Only logged in users can call this function. 
@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}, {session['email']}! <br/> <a href='/logout'><button>Logout</button></a>"

# Run the app. 
if __name__ == "__main__":
    app.run(debug=True)