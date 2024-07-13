from flask_security import Security, SQLAlchemyUserDatastore
from application.models import db, User, Role

datastore = SQLAlchemyUserDatastore(db, User, Role)
sec = Security()
