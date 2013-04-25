"""Declare the Koztumize application using Pynuts."""

import ldap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pynuts import Pynuts


class Koztumize(Pynuts):
    """The class which open the ldap."""
    @property
    def ldap(self):
        """Open the ldap."""
        try:  # pragma: no cover
            self.app.config.get('LDAP').search_s(
                self.app.config['LDAP_PATH'], ldap.SCOPE_ONELEVEL,
                'uid=Test')
        except:
            self.app.config['LDAP'] = ldap.open(self.app.config['LDAP_HOST'])
        return self.app.config['LDAP']


app = Flask(__name__)
app.config.from_envvar('KOZTUMIZE_CONFIG', silent=True)
app.db = SQLAlchemy(app)
nuts = Koztumize(app)
