"""Koztumize routes."""
# -*- coding: utf-8 -*-

import os
from flask import (
    g, render_template, request, redirect, url_for, jsonify, flash)
from pynuts.document import InvalidId
from pynuts.rights import allow_if
from . import rights as Is
from .application import nuts
from .directives import Button
from .document import CourrierStandard
from .helpers import NoPermission, get_last_commits
from .model import Users, UserRights, Rights, DB as db


@nuts.app.route('/')
@allow_if(Is.connected)
def index():
    """The index displays all the available models."""
    model_path = nuts.app.config['MODELS']
    models = {
        category: os.listdir(os.path.join(model_path, category))
        for category in os.listdir(model_path)
        if not category.startswith(('_', '.'))}
    commits = get_last_commits()
    return render_template('index.html', models=models, commits=commits)


@nuts.app.route('/create/<document_type>', methods=('GET', 'POST'))
@allow_if(Is.connected)
def create_document(document_type=None):
    """The route which renders the form for document creation.

    If POST, create the document by giving its type and its name.

    """
    if request.method == 'GET':
        return render_template(
            'document_form.html', document_type=document_type)
    else:
        document_name = request.form['name']
        if not document_name.replace(" ", ""):
            flash(u'Veuillez saisir un nom pour votre document !', 'error')
            return render_template(
                'document_form.html', document_type=document_type)
        for document in nuts.documents.values():
            if document_name in document.list_document_ids():
                flash(u'Un document porte déjà le même nom !', 'error')
                return render_template(
                    'document_form.html', document_type=document_type)
        document = nuts.documents[document_type]
        try:
            document.create(
                document_name=document_name,
                author_email=g.context.person.mail,
                author_name=g.context.person.fullname)
        except InvalidId:
            flash(
                'Erreur, veuillez ne pas mettre de "/" dans le nom de votre '
                'document.', 'error')
            return redirect(url_for(
                'create_document', document_type=document_type))
        db.session.add(Rights(document_name, g.context.person.user_id))
        db.session.add(
            UserRights(document_name, g.context.person.user_id, True, True))
        db.session.commit()
        return redirect(url_for(
            'edit', document_type=document_type, document_name=document_name))


@nuts.app.route('/edit/<document_type>/<path:document_name>')
@allow_if(Is.connected)
@allow_if(Is.document_writable, NoPermission)
def edit(document_name=None, document_type=None):
    """Render the page for document edition."""
    return render_template(
        'edit.html', document_type=document_type, document_name=document_name)


@nuts.app.route('/view/<document_type>/<path:document_name>/<version>')
@allow_if(Is.connected)
@allow_if(Is.document_readable, NoPermission)
def view(document_name=None, document_type=None, version=None):
    """Render the page for document view."""
    return render_template(
        'view.html', document_type=document_type, document_name=document_name,
        version=version)


@nuts.app.route('/documents')
@allow_if(Is.connected)
def documents():
    """Render the list of all the version of existing documents."""
    document_classes = nuts.documents.values()
    document_list = []
    for document_class in document_classes:
        document_ids = document_class.list_document_ids()
        for document_id in document_ids:
            users_read = []
            users_write = []
            allowed_users = UserRights.query.filter_by(
                document_id=document_id).all()
            for user in allowed_users:
                if user.read:
                    users_read.append(user.user_id)
                if user.write:
                    users_write.append(user.user_id)
            document_list.append({
                'document_id': document_id,
                'users_read': users_read,
                'users_write': users_write,
                'type': document_class.type_name,
                'history': list(document_class(document_id).history)})
    return render_template('documents.html', document_list=document_list)


@nuts.app.route('/model/<document_type>/<path:document_name>/head')
@nuts.app.route('/model/<document_type>/<path:document_name>/<version>')
@allow_if(Is.connected)
def model(document_name=None, document_type=None, version=None):
    """The route which renders the ReST model parsed in HTML."""
    document = nuts.documents[document_type]
    editable = False if version else True
    return document.html(
        'model.html', editable=editable, document_name=document_name,
        version=version)


@nuts.app.route('/pdf/<document_type>/<path:document_name>')
@nuts.app.route('/pdf/<document_type>/<path:document_name>/<version>')
@allow_if(Is.connected)
def pdf(document_type, document_name, version=None):
    """The route which returns a document as PDF."""
    document = nuts.documents[document_type]
    return document.download_pdf(
        document_name=document_name, filename=document_name + '.pdf',
        version=version)


# AJAX routes
@nuts.app.route('/create_rights', methods=('POST',))
def create_rights():
    """Grant specific rights to a document."""
    document_id = request.form['document_id']
    user_id = request.form['user_id']
    fullname = Users.query.get(user_id).fullname
    read = request.form['read']
    write = request.form['write']
    db.session.add(UserRights(document_id, user_id, read, write))
    db.session.commit()
    return jsonify({
        'user_id': user_id, 'fullname': fullname,
        'read': read, 'write': write})


@nuts.app.route('/read_rights/<document_id>')
def read_rights(document_id):
    """Render a list of users and their rights for the current document."""
    users = Users.query.all()
    allowed_users = UserRights.query.filter_by(document_id=document_id).all()
    allowed_user_ids = [user.user_id for user in allowed_users]
    owner = Rights.query.filter_by(document_id=document_id).first().owner
    available_users = [
        user for user in users if user.employe and
        user.user_id not in allowed_user_ids]
    return render_template(
        'rights.html', document_name=document_id, users=users,
        allowed_users=allowed_users, owner=owner,
        available_users=available_users)


@nuts.app.route('/delete_rights', methods=('POST',))
def delete_rights():
    """Remove rights for a document."""
    document_id = request.form['document_id']
    user_id = request.form['user_id']
    fullname = Users.query.get(user_id).fullname
    db.session.query(UserRights).filter_by(
        document_id=document_id, user_id=user_id).delete()
    db.session.commit()
    return jsonify({'user_id': user_id, 'fullname': fullname})


@nuts.app.route('/pdf_link/<string:document_type>/<string:document_name>')
def pdf_link(document_type, document_name):
    """Return the link for PDF downloading."""
    return url_for(
        'pdf', document_type=document_type, document_name=document_name)
