#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import ldap
import pytz
from urllib import unquote
from datetime import datetime
from operator import itemgetter
from heapq import nlargest
from flask import (render_template, request, redirect, url_for, jsonify,
                   session, current_app, flash)
from pynuts.rights import allow_if
from application import app
import rights as Is
from document import CourrierStandard
from directives import Button

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')

tz_paris = pytz.timezone('Europe/Paris')


def get_all_commits():
    repo = current_app.document_repository
    read_ref = repo.refs.read_ref
    return (
        {
            'message': commit.message.decode('utf-8'),
            'author': commit.author.decode('utf-8'),
            'date': datetime.utcfromtimestamp(commit.commit_time),
            'version': commit.id,
            'ref': tuple(unquote(ref).split('/', 1))}
        for ref in repo.refs.keys(base='refs/heads/documents/')
        for commit in repo.revision_history(
            read_ref('refs/heads/documents/' + ref))
    )


def get_last_commits(n=10):
    return nlargest(n, get_all_commits(), key=itemgetter('date'))


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
    commits = get_last_commits()
    return render_template('index.html', models=models, commits=commits)


@app.route('/create/<string:document_type>', methods=('GET', 'POST'))
@allow_if(Is.connected)
def create_document(document_type=None):
    if request.method == 'GET':
        return render_template('document_form.html',
                               document_type=document_type)
    else:
        document_name = request.form['name']
        document = current_app.documents[document_type]
        if document_name not in document.list_document_ids():
            document.create(document_name=document_name,
                            author_name=session.get('user'),
                            author_email=session.get('usermail'))
            return redirect(url_for('edit',
                                    document_type=document_type,
                                    document_name=document_name))
        else:
            flash('Un document porte déjà le même nom !'.decode('utf8'),
                  'error')
            return render_template('document_form.html',
                               document_type=document_type)


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
    document = current_app.documents[document_type]
    return document.html('model.html', document=document,
                         document_name=document_name, version=version)


@app.route('/pdf/<string:document_type>/<string:document_name>')
@app.route('/pdf/<string:document_type>/<string:document_name>/<version>')
@allow_if(Is.connected)
def pdf(document_type, document_name, version=None):
    document = app.documents[document_type]
    return document.download_pdf(document_name=document_name,
                                 filename=document_name + '.pdf',
                                 version=version)


# AJAX routes
@app.route('/save/<string:document_type>', methods=('POST', ))
@app.route('/save/<string:document_type>/<string:message>', methods=('POST', ))
def save(document_type, message=None):
    document = current_app.documents[document_type]
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
