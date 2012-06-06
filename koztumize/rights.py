from flask import session, request
from application import app
from pynuts.rights import acl
from model import Rights, UserRights


class Context(app.Context):
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
def connected():
    """Returns whether the user is connected."""
    return app.context.person is not None


#@acl
#def admin():
#    """Returns whether the user is connected."""
#    return session.get('user') == 'admin'


#@acl
#def in_his_domain():
#    return session.get('user_group') == request.host.split('.')[0]


#@acl
#def document_owner():
#    document = Rights.query.filter_by(
#        document_id=request.view_args['document_name']).first()
#    return app.context.person == document.owner


@acl
def document_readable():
    document_id = request.view_args['document_name']
    user_id = app.context.person
    rights = UserRights.query.filter_by(
        document_id=document_id, user_id=user_id).first()
    return rights and rights.read


@acl
def document_writable():
    document_id = request.view_args['document_name']
    user_id = app.context.person
    rights = UserRights.query.filter_by(
        document_id=document_id, user_id=user_id).first()
    return rights and rights.write
