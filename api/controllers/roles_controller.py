from api import db
from sqlalchemy.exc import SQLAlchemyError
from api.models.role import Role



####################### Jobs Info #####################
class RolesController: 
    
    def roles():
        roles = Role.query.all()
        serialzied = [j.serialize() for j in roles]
        return serialzied, 200
    
    def newRole(role):
        new_role = Role(role=role)
        try: 
            db.session.add(new_role)
            db.session.commit()

            return "", 204
        except SQLAlchemyError as e: 
            return "".format(e)
        return "", 200