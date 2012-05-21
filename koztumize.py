#! /usr/bin/env python2

import os
import ldap
from flask import (render_template, request, redirect, url_for, jsonify,
                   session, current_app, flash)
import pytz
from pynuts.rights import allow_if
from application import app
import rights as Is
from document import CourrierStandard
from directives import Button

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')

tz_paris = pytz.timezone('Europe/Paris')


@app.template_filter()
def local_time(datetime):
    return pytz.utc.localize(datetime).astimezone(tz_paris)

@app.template_filter()
def strftime(datetime, format):
    return datetime.strftime(format.encode('utf8')).decode('utf8')


@app.errorhandler(403)
@app.route('/login')
def login(error):
    return render_template('login.html')


@app.route('/login', methods=('POST', ))
def login_post():
    username = request.form['login']
    password = request.form['passwd']
    user = current_app.ldap.search_s(
        app.config['LDAP_PATH'], ldap.SCOPE_ONELEVEL, "uid=%s" % username)
    if not user or not password:
        flash(u"Erreur : Les identifiants sont incorrects.", 'error')
        return render_template('login.html')
    try:
        current_app.ldap.simple_bind_s(user[0][0], password)
    except ldap.INVALID_CREDENTIALS:  # pragma: no cover
        flash(u"Erreur : Les identifiants sont incorrects.", 'error')
        return render_template('login.html')
    session["user"] = user[0][1]['cn'][0].decode('utf-8')
    session["usermail"] = user[0][1].get('mail', ["none"])[0].decode('utf-8')
    return redirect(url_for('index'))


@app.route('/logout')
@allow_if(Is.connected)
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/')
@allow_if(Is.connected)
def index():
    model_path = app.config['MODELS']
    models = {
        category: os.listdir(os.path.join(model_path, category))
        for category in os.listdir(model_path)}
    return render_template('index.html', models=models)


@app.route('/create/<string:document_type>', methods=('GET', 'POST'))
@allow_if(Is.connected)
def create_document(document_type=None):
    if request.method == 'GET':
        return render_template('document_form.html',
                               document_type=document_type)
    else:
        document_name = request.form['name']
        document = app.documents[document_type]
        document.create(document_name=document_name,
                        author_name=session.get('user'),
                        author_email=session.get('usermail'))
        return redirect(url_for('edit',
                                document_type=document_type,
                                document_name=document_name))


@app.route('/edit/<string:document_type>/<string:document_name>')
@app.route('/edit/<string:document_type>/<string:document_name>/<version>')
@allow_if(Is.connected)
def edit(document_name=None, document_type=None, version=None):
    return render_template('edit.html', document_type=document_type,
                           document_name=document_name, version=version)


@app.route('/documents')
@allow_if(Is.connected)
def documents():
    return render_template('documents.html',
                           document_classes=app.documents.values())


@app.route('/model/<string:document_type>/<string:document_name>')
@app.route('/model/<string:document_type>/<string:document_name>/<version>')
@allow_if(Is.connected)
def model(document_name=None, document_type=None, version=None):
    document = app.documents[document_type]
    return document.html('model.html', document=document,
                         document_name=document_name, version=version)


@app.route('/pdf/<string:document_type>/<string:document_name>')
@allow_if(Is.connected)
def pdf(document_type, document_name):
    document = app.documents[document_type]
    return document.download_pdf(
        document_name=document_name, filename=document_name + '.pdf')


# AJAX routes
@app.route('/save/<string:document_type>', methods=('POST', ))
@app.route('/save/<string:document_type>/<string:message>', methods=('POST', ))
def save(document_type, message=None):
    document = app.documents[document_type]
    return jsonify(documents=document.update_content(
        request.json, author_name=session.get('user'),
        author_email=session.get('usermail'), message=message))


@app.route('/pdf_link/<string:document_type>/<string:document_name>')
def pdf_link(document_type, document_name):
    return url_for(
        'pdf', document_type=document_type, document_name=document_name)


if __name__ == '__main__':
    app.secret_key = 'Azerty'
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)
