from flask import request, render_template, redirect, Response, request
from api import db
from api.models.user import User
from sqlalchemy.exc import SQLAlchemyError



####################### Jobs Info #####################
class UsersController: 
    def users():
        users = User.query.all()
        serialzied = [j.serialize() for j in users]
        return serialzied, 200


    def newUser(google_id_input,name_input,email_input):
        new_user = User(
            google_id=google_id_input,
            name=name_input, 
            email=email_input, 
            role_id=1
        )
        try: 
            db.session.add(new_user)
            db.session.commit()

            return "", 204
        except SQLAlchemyError as e: 
            return "".format(e)
        return "", 200



    def showJob(id):
        return User.query.get(id).serialize(), 200
    