# -*- coding: utf-8 -*-

import os
import shutil
import pynuts
from tempfile import mkdtemp
from koztumize import application

PATH = os.path.dirname(os.path.dirname(__file__))


def execute_sql(app, filename, folder=None):
    """Execute a sql file in the sql folder for application.app"""
    if folder == 'tests':
        path = os.path.join(PATH, 'tests', 'sql', filename)
    else:
        path = os.path.join(PATH, 'sql', filename)
    with app.open_resource(path) as f:
        sql = f.read().decode('utf-8')
    app.db.session.execute(sql)
    app.db.session.commit()


def setup():
    if not os.path.exists(
        os.path.join(PATH, 'tests', 'fake_instance', 'documents.git')):
        shutil.copytree(
            os.path.join(PATH, 'tests', 'dump', 'instance', 'documents.git'),
            os.path.join(PATH, 'tests', 'fake_instance', 'documents.git'))
    config_file = os.path.join(PATH, 'config', 'test.cfg')
    app = application.Koztumize('koztumize', config_file=config_file)
    application.app = app
    execute_sql(app, 'db.sql', 'tests')
    from koztumize import routes
    

def teardown():
    """Remove the temp directory after the tests."""
    execute_sql(application.app, 'drop_all.sql', 'tests')
    shutil.rmtree(os.path.join(PATH, 'tests', 'fake_instance'))

