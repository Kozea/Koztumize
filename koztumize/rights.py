"""Koztumize document rights."""

from os import environ
from flask import request, g
from pynuts.rights import acl
from .application import nuts
from .model import Users, UserRights


class Context(nuts.Context):
    @property
    def person(self):
        """Get the current logged on person, or None."""
        return (
            Users.query
            .filter_by(uid=environ.get(
                'REMOTE_USER', 'palban' if nuts.app.debug else None))
            .one())


@acl
def connected(**params):
    """True when the user is connected."""
    return g.context.person is not None


def _document_access(_rights_type, **params):
    """True if the _rights_type is allowed for the current user."""
    document_id = request.view_args['document_name']
    user_id = g.context.person.user_id
    rights = UserRights.query.filter_by(
        document_id=document_id, user_id=user_id).first()
    return rights and getattr(rights, _rights_type)


@acl
def document_readable(**params):
    """True if a document is readable by the user."""
    return _document_access('read', **params)

@acl
def document_writable(**params):
    """True if a document is writable by the user."""
    return _document_access('write', **params)
