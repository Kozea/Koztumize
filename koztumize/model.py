"""Koztumize model classes."""

from .application import app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask.ext.sqlalchemy import SQLAlchemy


DB = SQLAlchemy(app)


class Rights(DB.Model):
    """Rights table."""
    document_id = DB.Column(DB.String(), primary_key=True)
    owner = DB.Column(DB.Integer)

    def __init__(self, doc_id, owner):
        self.document_id = doc_id
        self.owner = owner


class Users(DB.Model):
    """Users table."""
    user_id = DB.Column('uidNumber', DB.Integer, primary_key=True)
    name = DB.Column('sn', DB.String)
    firstname = DB.Column('givenName', DB.String)
    fullname = DB.Column('cn', DB.String)
    employe = DB.Column('employeeNumber', DB.Integer)
    uid = DB.Column('uid', DB.String, unique=True)
    mail = DB.Column('mail', DB.String, unique=True)


class UserRights(DB.Model):
    """User rights table."""
    document_id = DB.Column(DB.String(), primary_key=True)
    user_id = DB.Column(DB.Integer, primary_key=True)
    read = DB.Column(DB.Boolean)
    write = DB.Column(DB.Boolean)

    user = relationship(
        'Users', primaryjoin='UserRights.user_id == Users.user_id',
        foreign_keys=[Users.user_id], uselist=False)

    def __init__(self, doc_id, user_id, read=None, write=None):
        self.document_id = doc_id
        self.user_id = user_id
        self.read = read or False
        self.write = write or False
