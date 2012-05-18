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


CONFIG = {'PYNUTS_DOCUMENT_REPOSITORY': '/tmp/models.git',
          'LDAP_HOST': 'ldap.keleos.fr',
          'LDAP_PATH': 'ou=People,dc=keleos,dc=fr'}


app = Koztumize(__name__, config=CONFIG)
