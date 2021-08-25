import logging
import socket

from .c import Krb5
from .errors import TokenRetrievalError

__all__ = ("TokenProvider",)

_log = logging.getLogger("hzkerberos")


class TokenProvider(object):
    """TokenProvider is a Hazelcast token provider for Kerberos authentication.

    The provider tries to acquire and cache the Kerberos ticket if ``keytab`` arguments is given.

    Keyword Args:
        principal (`str`): Optional Kerberos principal. If provided, it will be used verbatim as the Kerberos principal. E.g., ``hz/127.0.0.1@EXAMPLE.COM``
        spn (`str`): Optional Service principal name (SPN). If provided (and principal is not provided) it will be used as the Kerberos principal,
            adding the realm if necessary. If not provided, it will be built using prefix, IP/host of the member and the realm. E.g., ``hz/127.0.0.1``
        prefix (`str`): Optional prefix for SPN, by default ``hz``.
        realm (`str`): Optional realm for SPN.
        canonical_hostname (`bool`): If ``true``, attempts to convert member IPs to hostnames. It is ``false`` by default.
        keytab (`str`): Optional keytab for the principal. If not provided, the library attempts to use an already cached ticket.
        libname (`str`): Optional Kerberos5 library name.
    """

    def __init__(
        self,
        principal="",
        spn="",
        prefix="hz",
        realm="",
        canonical_hostname=False,
        keytab="",
        libname="libkrb5.so",
    ):
        # type: (TokenProvider, str, str, str, str, bool, str, str) -> None
        self.principal = principal
        self.spn = spn
        self.prefix = prefix
        self.realm = realm
        self.canonical_hostname = canonical_hostname
        self.keytab = keytab
        self.__krb5 = Krb5(libname=libname)

    def token(self, address=None):
        # address.host is assumed to be the connected IP of the member
        if address:
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
            principal=principal, keytab=self.keytab
        )


def _make_principal(host, spn="", prefix="hz/", realm=""):
    if not spn:
        if prefix and not prefix.endswith("/"):
            prefix = "%s/" % prefix
        spn = "%s%s" % (prefix, host)
    if realm and "@" not in spn:
        spn = "%s@%s" % (spn, realm.upper())
    return spn


def _resolve_host(ip):
    # returns host name from the IP
    try:
        s = socket.gethostbyaddr(ip)
        return s[0]
    except (socket.herror, socket.gaierror) as e:
        raise TokenRetrievalError("%s: %s" % (e.args[1], ip))
    except socket.gaierror as e:
        raise TokenRetrievalError("%s: %s" % (e.args[1], ip))
    except:
        raise TokenRetrievalError("cannot resolve: %s" % ip)
