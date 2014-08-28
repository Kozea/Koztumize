"""Koztumize's helpers."""
# -*- coding: utf-8 -*-

import pytz
from heapq import nlargest
from operator import itemgetter
from datetime import datetime as dt
from urllib import unquote
import locale
from flask import render_template, flash, redirect
from .application import nuts

# TODO: this should be configurable, of course
locale.setlocale(locale.LC_ALL, 'fr_FR')
TZ = pytz.timezone('Europe/Paris')


class NoPermission(Exception):
    """Exception raised for denying access on documents."""


def get_all_commits():
    repo = nuts.document_repository
    read_ref = repo.refs.read_ref
    return (
        {'message': entry.commit.message.decode('utf-8'),
         'author': entry.commit.author.decode('utf-8'),
         'date': dt.utcfromtimestamp(entry.commit.commit_time),
         'version': entry.commit.id,
         'ref': tuple(unquote(ref).split('/', 1))}
        for ref in repo.refs.keys(base='refs/heads/documents/')
        for entry in repo.get_walker(
            include=[read_ref('refs/heads/documents/' + ref)])
        if entry.commit.parents)


def get_last_commits(number=10):
    """Get the n latest commits."""
    return nlargest(number, get_all_commits(), key=itemgetter('date'))


@nuts.app.template_filter()
def localtime(datetime):
    """Get the local time according to your timezone."""
    return pytz.utc.localize(datetime).astimezone(TZ)


@nuts.app.template_filter()
def strftime(datetime, formattime):
    return datetime.strftime(formattime.encode('utf8')).decode('utf8')


@nuts.app.errorhandler(403)
def forbidden(error):
    """Forbidden error handler."""
    return render_template('forbidden.html'), 403


@nuts.app.errorhandler(NoPermission)
def no_permission(error):
    """NoPermission error handler."""
    flash(u'Vous n’avez pas l’autorisation d’accéder à ce document.', 'error')
    return redirect('/')
