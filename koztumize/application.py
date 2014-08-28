"""Declare the Koztumize application using Pynuts."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pynuts import Pynuts

app = Flask(__name__)
app.config.from_envvar('KOZTUMIZE_CONFIG', silent=True)
app.db = SQLAlchemy(app)
nuts = Pynuts(app)
