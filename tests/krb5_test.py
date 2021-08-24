import os
import unittest

import hzkerberos
from hzkerberos.c import Krb5
from .util import make_principal, default_keytab, Address


class Krb5Test(unittest.TestCase):
    default_address = None

    @classmethod
    def setUpClass(cls):
        cls.default_address = Address(host="hz1", resolve=True)

    @classmethod
    def tearDownClass(cls):
        krb5 = Krb5()
        krb5._destroy_cache()

    def test_get_token_with_keytab(self):
        p = hzkerberos.TokenProvider(keytab=default_keytab())
        tok = p.token(address=self.default_address)
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

    def test_get_token_with_cached_creds(self):
        # login and cache the ticket
        os.system("echo Password01 | kinit jduke@EXAMPLE.COM")
        # use cached ticket
        p = hzkerberos.TokenProvider()
        tok = p.token(address=self.default_address)
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

    def test_get_token_realm_unknown_failure(self):
        principal = make_principal(realm="foo.com")
        p = hzkerberos.TokenProvider(principal=principal, keytab="foo")
        self.assertRaisesRegex(
            hzkerberos.KerberosError,
            "KRB5_REALM_UNKNOWN",
            lambda: p.token(address=self.default_address),
        )

    def test_get_token_principal_unknown_failure(self):
        # unknown username
        principal = make_principal(prefix="hz2")
        p = hzkerberos.TokenProvider(principal=principal, keytab="foo")
        self.assertRaisesRegex(
            hzkerberos.KerberosError,
            "KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN",
            lambda: p.token(address=self.default_address),
        )
