# -*- coding: utf-8 -*-

import pytz
from .application import app
from heapq import nlargest
from operator import itemgetter
from datetime import datetime
from urllib import unquote
import locale
from flask import render_template, current_app, flash, redirect, request
locale.setlocale(locale.LC_ALL, 'fr_FR')

tz_paris = pytz.timezone('Europe/Paris')


class NoPermission(Exception):
    """TODO"""


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
        if commit.parents
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
def login(error):
    return render_template('login.html'), 403


@app.errorhandler(NoPermission)
def no_permission(error):
    flash(u"Vous n'avez pas l'autorisation d'accéder à cette page.", "error")
    return redirect(request.referrer)
