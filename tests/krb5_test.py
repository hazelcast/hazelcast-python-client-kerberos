import unittest

import hzkerberos
from .util import make_principal, default_keytab


class Krb5Test(unittest.TestCase):
    def test_get_token_with_password(self):
        p = hzkerberos.TokenProvider(principal=make_principal(prefix="hz1"), password="Password01")
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

    def test_get_token_with_keytab(self):
        p = hzkerberos.TokenProvider(principal=make_principal(), keytab=default_keytab())
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

        # leaving out keytab should work, since credentials are cached
        p = hzkerberos.TokenProvider(principal=make_principal())
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

    def test_get_token_realm_unknown_failure(self):
        principal = make_principal(realm="foo.com")
        p = hzkerberos.TokenProvider(principal=principal, password="Password01")
        self.assertRaisesRegex(hzkerberos.KerberosError, "KRB5_REALM_UNKNOWN", lambda: p.token())

    def test_get_token_principal_unknown_failure(self):
        # unknown username
        principal = make_principal(prefix="hz2")
        p = hzkerberos.TokenProvider(principal=principal, password="Password01")
        self.assertRaisesRegex(
            hzkerberos.KerberosError, "KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN", lambda: p.token()
        )

    def test_get_token_preauth_failure(self):
        # wrong password
        p = hzkerberos.TokenProvider(principal=make_principal(), password="wrongpassw0rd")
        self.assertRaisesRegex(
            hzkerberos.KerberosError, "KRB5KDC_ERR_PREAUTH_FAILED", lambda: p.token()
        )
