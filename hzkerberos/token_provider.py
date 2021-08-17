from .c import Krb5


class TokenProvider(object):
    """TokenProvider is a Hazelcast token provider for Kerberos authentication.

    The provider tries to acquire and credentials if one of
    ``password`` or ``keytab`` arguments is given. ``password`` and ``keytab`` are mutually exclusive,
    at most one of them should be specified.

    Args:
        spn (`str`): Service principal name. E.g., ``hz/127.0.0.1@EXAMPLE.COM``

    Keyword Args:
        password (`str`): Optional password for the principal.
        keytab (`str`): Optional keytab for the principal.
        libname (`str`): Optional Kerberos5 library name.
    """

    def __init__(self, spn, password="", keytab="", libname="libkrb5.so"):
        # type: (TokenProvider, str, str, str, str) -> None
        if not spn:
            raise ValueError("spn is required")
        self.spn = spn
        if password and keytab:
            raise ValueError("password and keytab parameters are mutually exclusive")
        self.password = password
        self.keytab = keytab
        self.__krb5 = Krb5(libname=libname)

    def token(self):
        # type: (TokenProvider) -> bytes
        return self.__krb5.get_token(principal=self.spn, password=self.password, keytab=self.keytab)
