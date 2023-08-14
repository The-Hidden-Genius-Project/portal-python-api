from app import Portal
from json # figure out how to import this json
app = Portal()
db  = app.db

@app.route('/')
def index():
    return jsonify() # this is where you will return a json objec to a jobro