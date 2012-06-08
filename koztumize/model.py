"""Koztumize model classes."""

from koztumize.application import app
from flask.ext.sqlalchemy import SQLAlchemy


DB = SQLAlchemy(app)


class Rights(DB.Model):
    """Class for Rights table."""
    document_id = DB.Column(DB.Integer, primary_key=True)
    owner = DB.Column(DB.String(), unique=True)

    def __init__(self, doc_id, owner):
        self.document_id = doc_id
        self.owner = owner


class UserRights(DB.Model):
    """Class for User_rights table."""
    document_id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(), primary_key=True)
    read = DB.Column(DB.Boolean, unique=True)
    write = DB.Column(DB.Boolean, unique=True)

    def __init__(self, doc_id, user_id, read=None, write=None):
        self.document_id = doc_id
        self.user_id = user_id
        self.read = read or False
        self.write = write or False


class Users(DB.Model):
    """Class for User table."""
    user_id = DB.Column('uidNumber', DB.Integer, primary_key=True)
    name = DB.Column('sn', DB.String)
    firstname = DB.Column('givenName', DB.String)
    fullname = DB.Column('cn', DB.String)
    employe = DB.Column('employeeNumber', DB.Integer)
