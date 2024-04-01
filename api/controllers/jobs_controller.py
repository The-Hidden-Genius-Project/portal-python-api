from flask import request, render_template, redirect, Response, request
from api import db
from sqlalchemy.exc import SQLAlchemyError
from api.models.job import Job

####################### Jobs Info #####################

class JobsController: 

    def jobs():
        jobs = Job.query.all()
        serialzied = [j.serialize() for j in jobs]
        return serialzied, 200

    def newJob(job_title, job_description, job_type, job_partner_id, job_organization_id):
        new_job = Job(
            title=job_title, 
            description=job_description, 
            type=job_type, 
            partner_id=job_partner_id, 
            organization_id=job_organization_id
        )
        try: 
            db.session.add(new_job)
            db.session.commit()

            return "", 204
        except SQLAlchemyError as e: 
            return "".format(e)
        return "", 200


    def showJob(id):
        return Job.query.get(id).serialize(), 200