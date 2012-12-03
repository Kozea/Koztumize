"""Koztumize document rights."""

from flask import session, request, g
from pynuts.rights import acl
from .application import nuts
from .model import UserRights


class Context(nuts.Context):
    """This class create a context. You can add properties like and use methods
       in order to make rights. Your rights methods have to be decorated by
       `@acl` for access control in `allow_if` decorators. `allow_if` checks
       that the global context matches a criteria.

    """

    @property
    def person(self):
        """Returns the current logged on person, or None."""
        return session.get('user')


@acl
def connected(**params):
    """Returns whether the user is connected."""
    return g.context.person is not None


@acl
def document_readable(**params):
    """Return if a document is readable by the user."""
    document_id = request.view_args['document_name']
    user_id = g.context.person
    rights = UserRights.query.filter_by(
        document_id=document_id, user_id=user_id).first()
    return rights and rights.read


@acl
def document_writable(**params):
    """Return if a document is writable by the user."""
    document_id = request.view_args['document_name']
    user_id = g.context.person
    rights = UserRights.query.filter_by(
        document_id=document_id, user_id=user_id).first()
    return rights and rights.write
