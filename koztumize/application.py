"""Declare the Koztumize application using Pynuts."""

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


app = Koztumize(
    __name__, config_file='config/config.cfg')  # pylint: disable=C0103
