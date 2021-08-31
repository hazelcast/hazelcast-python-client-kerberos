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
        principal (`str`): Optional Kerberos principal. If provided, it will be used as the Kerberos principal. E.g., ``jduke@EXAMPLE.COM``
        keytab (`str`): Optional keytab for the principal. If not provided, the library attempts to use an already cached ticket.
            Should not be used together with the ``password`` option.
        password (`str`): Optional password for the principal. If not provided, the library attempts to use an already cached ticket.
            Should not be used together with the ``keytab`` option.
        spn (`str`): Optional Service principal name (SPN). If not provided, it will be built using prefix, IP/host of the member and the realm. E.g., ``hz/127.0.0.1@EXAMPLE.COM``.
        prefix (`str`): Optional prefix for SPN, by default ``hz/``.
        realm (`str`): Optional realm for SPN.
        canonical_hostname (`bool`): If ``true``, attempts to convert member IPs to hostnames when building the SPN. It is ``false`` by default.
        libname (`str`): Optional Kerberos5 library name.
    """

    def __init__(
        self,
        principal="",
        keytab="",
        password="",
        spn="",
        prefix="hz",
        realm="",
        canonical_hostname=False,
        libname="libkrb5.so",
    ):
        # type: (TokenProvider, str, str, str, str, str, str, bool, str) -> None
        if principal:
            if not keytab and not password:
                raise ValueError("keytab or password is required when the principal is specified")
        if keytab and password:
            raise ValueError("keytab and password are mutually exclusive")
        self.principal = principal
        self.spn = spn
        self.prefix = prefix
        self.realm = realm
        self.keytab = keytab
        self.password = password
        self.canonical_hostname = canonical_hostname
        self.__krb5 = Krb5(libname=libname)

    def token(self, address=None):
        if not address:
            raise TokenRetrievalError("address is required")
        _log.debug("token host: %s", address.host)
        principal = self.principal
        host = address.host
        if self.canonical_hostname:
            host = _resolve_host(host)
        spn = _make_spn(host, self.spn, self.prefix, self.realm)
        _log.debug("token principal: %s", principal)
        _log.debug("token SPN: %s", spn)
        return self.__krb5.get_token(
            principal=principal,
            spn=spn,
            password=self.password,
            keytab=self.keytab,
        )


def _make_spn(host, spn="", prefix="hz/", realm=""):
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
    except:
        raise TokenRetrievalError("cannot resolve: %s" % ip)
