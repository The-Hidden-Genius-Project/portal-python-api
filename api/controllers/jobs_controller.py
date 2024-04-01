from flask import request, render_template, redirect, Response
from api import Initialize_Portal
from api.models.job import Job
from sqlalchemy.exc import SQLAlchemyError

# importing the necessary th
from app import db

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