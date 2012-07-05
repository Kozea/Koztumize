# -*- coding: utf-8 -*-

# Copyright (C) 2011 Kozea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Test for Koztumize (all the routes are tested)

"""

import json
import ldap
from flask import url_for
from .helpers import with_client, request
from koztumize import application
from nose.tools import raises


@with_client
@raises(ldap.INVALID_CREDENTIALS)
def test_login_post(client):
    """Test the login post."""
    with client.application.test_request_context():
        response = request(
            client.post, url_for('login_post'),
            data={'login': 'Tester', 'passwd': ''})
        assert 'Erreur : Les identifiants sont incorrects.' in response.data
        response = request(
            client.post, url_for('login_post'),
            data={'login': 'fake_login', 'passwd': 'fake_passwd'})


@with_client
def test_logout(client):
    """Test the logout."""
    with client.application.test_request_context():
        response = request(client.get, url_for('logout'))
        assert 'Veuillez vous connecter' in response.data
        response = request(client.get, '/', status_code=403)


@with_client
def test_index(client):
    """Test the index page."""
    with client.application.test_request_context():
        response = request(client.get, '/')
        assert 'Koztumize' in response.data
        assert 'Test' in response.data
        assert 'test' in response.data


@with_client
def test_create_document(client):
    """Test the document creation."""
    with client.application.test_request_context():
        response = request(client.get, url_for('create_document',
            document_type='test'))
        assert 'Veuillez choisir un nom pour le document' in response.data
        response = request(client.post, url_for('create_document',
            document_type='test'), data={'name': 'Test/test'})
        assert (
            '<p class="error">Erreur, veuillez ne pas mettre de &#34;/&#34; '
            'dans le nom de votre document.</p>'
            in response.data)
        response = request(client.post, url_for('create_document',
            document_type='test'), data={'name': ''})
        assert '<p class="error">Veuillez saisir un nom pour votre document' \
            in response.data
        response = request(client.post, url_for('create_document',
            document_type='test'), data={'name': 'First test'})
        assert 'teddybar' in response.data
        response = request(client.post, url_for('create_document',
            document_type='test'), data={'name': 'First test'})
        assert '<p class="error">Un document porte déjà le même nom' \
            in response.data


@with_client
def test_edit(client):
    """Test the edit page."""
    with client.application.test_request_context():
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert '<iframe>' in response.data
        assert '/model/test/First%20test/head' in response.data
        client.get('/logout')
        client.post('login', data={'login': 'Tester 2', 'passwd': 'tester2'})
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert (
            '<p class="error">Vous n&#39;avez pas l&#39;autorisation '
            'd&#39;accéder à cette page.</p>'
            in response.data)


@with_client
def test_view(client):
    """Test the view page."""
    with client.application.test_request_context():
        version = application.app.documents['test']('First test').version
        response = request(client.get, url_for(
            'view', document_type='test', document_name='First test',
            version=version))
        assert 'teddybar' not in response.data


@with_client
def test_model(client):
    """Test the model page."""
    with client.application.test_request_context():
        response = request(client.get, url_for(
            'model', document_type='test', document_name='First test'))
        assert 'contenteditable' in response.data


@with_client
def test_documents(client):
    """Test the documents page."""
    with client.application.test_request_context():
        response = request(client.get, url_for('documents'))
        data = '<a href="/edit/test/First%20test">First test</a>'
        assert data in response.data


@with_client
def test_pdf_link(client):
    """Test the PDF link page."""
    with client.application.test_request_context():
        response = request(client.get, url_for(
        'pdf_link', document_type='test', document_name='First test'))
        assert '/pdf/test/First%20test' in response.data


@with_client
def test_pdf(client):
    """Test the PDF generation page."""
    with client.application.test_request_context():
        response = request(client.get, url_for(
        'pdf', document_type='test', document_name='First test'),
        content_type='application/pdf')
        assert response.data[:4] == '%PDF'


@with_client
def test_rights(client):
    """Test the rights."""
    #Test create_rights
    with client.application.test_request_context():
        data = {
            'document_id': 'First test',
            'user_id': 'Tester 2',
            'read': 't',
            'write': 'f'}
        response = request(
            client.post,
            url_for('create_rights'),
            content_type='application/json',
            data=data)

        client.get('logout')
        client.post('login', data={'login': 'Tester 2', 'passwd': 'tester2'})

        #Test read right
        version = application.app.documents['test']('First test').version
        response = request(client.get, url_for(
            'view', document_type='test', document_name='First test',
            version=version))
        assert 'teddybar' not in response.data

        #Test write right
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert (
            '<p class="error">Vous n&#39;avez pas l&#39;autorisation '
            'd&#39;accéder à cette page.</p>'
            in response.data)

        client.get('logout')
        client.post('login', data={'login': 'Tester', 'passwd': 'tester'})

        #Test read_rights
        response = request(
            client.post,
            url_for('read_rights'), data={'document_id': 'First test'})
        assert '<div>Qui a acc\xc3\xa8s</div>' in response.data

        #Test update_rights
        #Allow only read
        version = application.app.documents['test']('First test').version
        data = {
            'document_id': 'First test',
            'user_id': 'Tester 2',
            'rights': 'r'}
        response = request(
            client.post,
            url_for('update_rights'),
            content_type='application/json',
            data=data)
        assert 'Lecture' in response.data

        client.get('logout')
        client.post('login', data={'login': 'Tester 2', 'passwd': 'tester2'})

        #Test write right
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert (
            '<p class="error">Vous n&#39;avez pas l&#39;autorisation '
            'd&#39;accéder à cette page.</p>'
            in response.data)

        #Test read right
        response = request(client.get, url_for(
            'view', document_type='test', document_name='First test',
            version=version))
        assert 'teddybar' not in response.data

        client.get('logout')
        client.post('login', data={'login': 'Tester', 'passwd': 'tester'})

        #Allow only write
        data = {
            'document_id': 'First test',
            'user_id': 'Tester 2',
            'rights': 'w'}
        response = request(
            client.post,
            url_for('update_rights'),
            content_type='application/json',
            data=data)
        assert 'Ecriture' in response.data

        client.get('logout')
        client.post('login', data={'login': 'Tester 2', 'passwd': 'tester2'})

        #Test write right
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert 'teddybar' in response.data

        #Test read right
        response = request(client.get, url_for(
            'view', document_type='test', document_name='First test',
            version=version))
        assert (
            '<p class="error">Vous n&#39;avez pas l&#39;autorisation '
            'd&#39;accéder à cette page.</p>'
            in response.data)
        client.get('logout')
        client.post('login', data={'login': 'Tester', 'passwd': 'tester'})

        #Allow both read & write
        data = {
            'document_id': 'First test',
            'user_id': 'Tester 2',
            'rights': 'rw'}
        response = request(
            client.post,
            url_for('update_rights'),
            content_type='application/json',
            data=data)
        assert 'Lecture et Ecriture' in response.data

        client.get('logout')
        client.post('login', data={'login': 'Tester 2', 'passwd': 'tester2'})

        #Test write right
        response = request(client.get, url_for(
            'edit', document_type='test', document_name='First test'))
        assert 'teddybar' in response.data

        #Test read right
        response = request(client.get, url_for(
            'view', document_type='test', document_name='First test',
            version=version))
        assert 'teddybar' not in response.data

        client.get('logout')
        client.post('login', data={'login': 'Tester', 'passwd': 'tester'})

        #Test delete_rights
        data = {
            'document_id': 'First test',
            'user_id': 'Tester 2'}
        response = request(
            client.post,
            url_for('delete_rights'),
            data=data)
        assert 'Tester 2' in response.data


@with_client
def test_save(client):
    """Test the document saving."""
    with client.application.test_request_context():
        version = application.app.documents['test']('First test').version
        data = json.dumps([{
            'document_type': 'test',
            'document_id': 'First test',
            'version': version,
            'part': 'Date',
            'content': '05/06/2012'}])
        response = request(
            client.post,
            url_for('save', document_type='test'),
            content_type='application/json',
            data_content_type='application/json',
            data=data)
        response_data = json.loads(response.data)
        assert 'test' in response.data
        assert version != response_data['documents'][0]['version']
