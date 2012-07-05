"""Declare the Koztumize application using Pynuts."""

import os
import ldap
from pynuts import Pynuts


class Koztumize(Pynuts):
    """The class which open the ldap."""
    @property
    def ldap(self):
        """Open the ldap."""
        if 'LDAP' not in self.config:  # pragma: no cover
            self.config['LDAP'] = ldap.open(self.config['LDAP_HOST'])
        return self.config['LDAP']


app = Koztumize(  # pylint: disable=E1101
    __name__, config_file=os.environ.get('KOZTUMIZE_CONFIG'))
