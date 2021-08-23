import logging
import socket

from .c import Krb5
from .errors import TokenRetrievalError

__all__ = ("TokenProvider",)

_log = logging.getLogger("hzkerberos")


class TokenProvider(object):
    """TokenProvider is a Hazelcast token provider for Kerberos authentication.

    The provider tries to acquire and credentials if one of
    ``password`` or ``keytab`` arguments is given. ``password`` and ``keytab`` are mutually exclusive,
    at most one of them should be specified.

    Keyword Args:
        principal (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        spn (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        prefix (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        realm (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        canonical_hostname (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        keytab (`str`): Optional keytab for the principal.
        password (`str`): Optional password for the principal.
        libname (`str`): Optional Kerberos5 library name.
    """

    def __init__(
        self,
        principal="",
        spn="",
        prefix="hz/",
        realm="",
        canonical_hostname=False,
        keytab="",
        password="",
        libname="libkrb5.so",
    ):
        # type: (TokenProvider, str, str, str, str, bool, str, str, str) -> None
        if password and keytab:
            raise ValueError("password and keytab parameters are mutually exclusive")
        self.principal = principal
        self.spn = spn
        self.prefix = prefix
        self.realm = realm
        self.canonical_hostname = canonical_hostname
        self.password = password
        self.keytab = keytab
        self.__krb5 = Krb5(libname=libname)

    def token(self, address=None):
        # address.host is assumed to be the connected IP of the member
        _log.debug("token host: %s", address.host)
        principal = self.principal
        if not principal:
            if not address:
                raise TokenRetrievalError("address is required when principal is not given")
            host = address.host
            if self.canonical_hostname:
                host = _resolve_host(host)
            principal = _make_principal(host, self.spn, self.prefix, self.realm)
        _log.debug("token principal: %s", principal)
        return self.__krb5.get_token(
            principal=principal, password=self.password, keytab=self.keytab
        )


def _make_principal(host, spn="", prefix="hz/", realm=""):
    if not spn:
        spn = "%s%s" % (prefix, host)
    if realm:
        spn = "%s@%s" % (spn, realm.upper())
    return spn


def _resolve_host(ip):
    # returns host name from the IP
    try:
        s = socket.gethostbyaddr(ip)
        return s[0]
    except socket.herror as e:
        raise TokenRetrievalError("%s: %s" % (e.args[1], ip))
    except socket.gaierror as e:
        raise TokenRetrievalError("%s: %s" % (e.args[1], ip))
    except:
        raise TokenRetrievalError("cannot resolve: %s" % ip)
