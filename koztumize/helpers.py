"""Koztumize's helpers."""
# -*- coding: utf-8 -*-

import pytz
from .application import app
from heapq import nlargest
from operator import itemgetter
from datetime import datetime as dt
from urllib import unquote
import locale
from flask import render_template, current_app, flash, redirect
locale.setlocale(locale.LC_ALL, 'fr_FR')

TZ_PARIS = pytz.timezone('Europe/Paris')


class NoPermission(Exception):
    """Exception raised for denying access on documents."""


def get_all_commits():
    repo = current_app.document_repository
    read_ref = repo.refs.read_ref
    return (
        {
            'message': commit.message.decode('utf-8'),
            'author': commit.author.decode('utf-8'),
            'date': dt.utcfromtimestamp(commit.commit_time),
            'version': commit.id,
            'ref': tuple(unquote(ref).split('/', 1))}
        for ref in repo.refs.keys(base='refs/heads/documents/')
        for commit in repo.revision_history(
            read_ref('refs/heads/documents/' + ref))
        if commit.parents
    )


def get_last_commits(number=10):
    """Get the n latest commits."""
    return nlargest(number, get_all_commits(), key=itemgetter('date'))


@app.template_filter()
def local_time(datetime):
    """Return the local time according to your timezone."""
    return pytz.utc.localize(datetime).astimezone(TZ_PARIS)  # pragma: no cover


@app.template_filter()
def strftime(datetime, formattime):
    return datetime.strftime(
        formattime.encode('utf8')).decode('utf8')  # pragma: no cover


@app.errorhandler(403)
def login(error):
    """Forbidden error handler."""
    return render_template('login.html'), 403


@app.errorhandler(NoPermission)
def no_permission(error):
    """NoPermission error handler."""
    flash(u"Vous n'avez pas l'autorisation d'accéder à cette page.", "error")
    return redirect('/')
