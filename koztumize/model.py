from application import app
from flask.ext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://koztumize:koztumize@macaron/koztumize"

db = SQLAlchemy(app)


class Rights(db.Model):
    document_id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(), unique=True)

    def __init__(self, doc_id, owner):
        self.document_id = doc_id
        self.owner = owner


class UserRights(db.Model):
    document_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), primary_key=True)
    read = db.Column(db.Boolean, unique=True)
    write = db.Column(db.Boolean, unique=True)

    def __init__(self, doc_id, user_id, read=None, write=None):
        self.document_id = doc_id
        self.user_id = user_id
        self.read = read or False
        self.write = write or False


class Users(db.Model):
    user_id = db.Column('uidNumber', db.Integer, primary_key=True)
    name = db.Column('sn', db.String)
    firstname = db.Column('givenName', db.String)
    fullname = db.Column('cn', db.String)
    employe = db.Column('employeeNumber', db.Integer)
