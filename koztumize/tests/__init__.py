# -*- coding: utf-8 -*-

import os
import shutil
import pynuts
from tempfile import mkdtemp
from brigit import Git
from koztumize import application

PATH = os.path.dirname(os.path.dirname(__file__))
TEMP_DIR = None


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
    # global variable shouldn't be used but is quite useful here
    # pylint: disable=W0603
    global TEMP_DIR
    TEMP_DIR = mkdtemp()
    if not os.path.exists(
        os.path.join(PATH, 'tests', 'fake_instance', 'documents.git')):
        shutil.copytree(
            os.path.join(PATH, 'tests', 'dump', 'instance', 'documents.git'),
            os.path.join(PATH, 'tests', 'fake_instance', 'documents.git'))
    config_file = os.path.join(PATH, 'config', 'test.cfg')
    app = application.Koztumize('koztumize', config_file=config_file)
    application.app = app
    app.config['MODELS'] = os.path.join(TEMP_DIR, 'models')
    git = Git(app.config['MODELS'])
    git.init()
    git.remote('add', '-t', 'models', 'origin', app.config['GIT_REMOTE'])
    git.pull()
    git.checkout('models')
    execute_sql(app, 'db.sql', 'tests')
    from koztumize import routes
    import document
    

def teardown():
    """Remove the temp directory after the tests."""
    execute_sql(application.app, 'drop_all.sql', 'tests')
    if os.path.exists(os.path.join(PATH, 'tests', 'fake_instance')):
        shutil.rmtree(os.path.join(PATH, 'tests', 'fake_instance'))
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
