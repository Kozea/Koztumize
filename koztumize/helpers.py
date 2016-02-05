"""Koztumize's helpers."""
# -*- coding: utf-8 -*-

import pytz
from .application import nuts
from heapq import nlargest
from operator import itemgetter
from datetime import datetime as dt
from urllib import unquote
import locale
from flask import render_template, flash, redirect
locale.setlocale(locale.LC_ALL, 'fr_FR')

TZ_PARIS = pytz.timezone('Europe/Paris')


class NoPermission(Exception):
    """Exception raised for denying access on documents."""


def get_all_commits():
    repo = nuts.document_repository
    read_ref = repo.refs.read_ref
    return (
	{
            'message': result.commit.message.decode('utf-8'),
            'author': result.commit.author.decode('utf-8'),
            'date': dt.utcfromtimestamp(result.commit.commit_time),
            'version': result.commit.id,
            'ref': tuple(unquote(ref).split('/', 1))}
        for ref in repo.refs.keys(base='refs/heads/documents/')
        for result in repo.get_walker(
            read_ref('refs/heads/documents/' + ref))
        if result.commit.parents
    )


def get_last_commits(number=10):
    """Get the n latest commits."""
    return nlargest(number, get_all_commits(), key=itemgetter('date'))


@nuts.app.template_filter()
def local_time(datetime):
    """Return the local time according to your timezone."""
    return pytz.utc.localize(datetime).astimezone(TZ_PARIS)  # pragma: no cover


@nuts.app.template_filter()
def strftime(datetime, formattime):
    return datetime.strftime(
        formattime.encode('utf8')).decode('utf8')  # pragma: no cover


@nuts.app.errorhandler(403)
def login(error):
    """Forbidden error handler."""
    return render_template('login.html'), 403


@nuts.app.errorhandler(NoPermission)
def no_permission(error):
    """NoPermission error handler."""
    flash(u"Vous n'avez pas l'autorisation d'accéder à cette page.", "error")
    return redirect('/')
