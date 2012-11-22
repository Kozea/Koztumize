"""Init file for koztumize tests"""
# -*- coding: utf-8 -*-

import os
import shutil
from tempfile import mkdtemp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from brigit import Git

from . import config
from .. import application

PATH = os.path.dirname(os.path.dirname(__file__))
TEMP_DIR = None
FAKE_DIR = os.path.join(PATH, 'tests', 'fake_instance')


def execute_sql(app, filename, folder=None):
    """Execute a sql file in the sql folder for application.app"""
    if folder == 'tests':
        path = os.path.join(PATH, 'tests', 'sql', filename)
    else:
        path = os.path.join(PATH, 'sql', filename)
    with app.open_resource(path) as sqlfile:
        sql = sqlfile.read().decode('utf-8')
    app.db.session.execute(sql)
    app.db.session.commit()


def setup():
    """Setup function for tests."""
    # global variable shouldn't be used but is quite useful here
    # pylint: disable=W0603
    global TEMP_DIR
    TEMP_DIR = mkdtemp()
    if not os.path.exists(FAKE_DIR):
        os.mkdir(FAKE_DIR)
        Git(os.path.join(FAKE_DIR, 'documents.git')).init()
    app = Flask(
        __name__,
        static_folder=os.path.join(PATH, 'static'),
        template_folder=os.path.join(PATH, 'templates'))
    app.config.from_object(config)
    app.db = SQLAlchemy(app)
    nuts = application.Koztumize(app)
    application.app = app
    application.nuts = nuts
    app.config['MODELS'] = os.path.join(TEMP_DIR, 'models')
    git = Git(app.config['MODELS'])
    git.init()
    git.remote('add', '-t', 'models', 'origin', app.config['GIT_REMOTE'])
    git.pull()
    git.checkout('models')
    execute_sql(app, 'db.sql', 'tests')
    import koztumize.routes
    import koztumize.tests.document


def teardown():
    """Remove the temp directory after the tests."""
    execute_sql(application.app, 'drop_all.sql', 'tests')
    if os.path.exists(os.path.join(PATH, 'tests', 'fake_instance')):
        shutil.rmtree(os.path.join(PATH, 'tests', 'fake_instance'))
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
