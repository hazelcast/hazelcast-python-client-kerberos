import unittest

import hzkerberos
from .util import make_principal, default_keytab


class Krb5TestCase(unittest.TestCase):

    # def test_get_token_with_password(self):
    #     p = hzkerberos.TokenProvider(spn=make_principal(), password="Password01")
    #     tok = p.token()
    #     self.assertIsNotNone(tok)
    #     self.assertIsInstance(tok, bytes)

    def test_get_token_with_keytab(self):
        p = hzkerberos.TokenProvider(spn=make_principal(), keytab=default_keytab())
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

        # leaving out keytab should work, since credentials are cached
        p = hzkerberos.TokenProvider(spn=make_principal())
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)

    def test_get_token_realm_unknown_failure(self):
        principal = make_principal(realm="foo.com")
        p = hzkerberos.TokenProvider(spn=principal, password="Password01")
        try:
            _ = p.token()
        except hzkerberos.KerberosError as ex:
            self.assertIn("KRB5_REALM_UNKNOWN", ex.args[0])
        else:
            self.fail("should have failed")

    def test_get_token_principal_unknown_failure(self):
        # unknown username
        principal = make_principal(prefix="hz1")
        p = hzkerberos.TokenProvider(spn=principal, password="Password01")
        try:
            _ = p.token()
        except hzkerberos.KerberosError as ex:
            self.assertIn("KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN", ex.args[0])
        else:
            self.fail("should have failed")

    def test_get_token_preauth_failure(self):
        # wrong password
        p = hzkerberos.TokenProvider(spn=make_principal(), password="wrongpassw0rd")
        try:
            _ = p.token()
        except hzkerberos.KerberosError as ex:
            self.assertIn("KRB5KDC_ERR_PREAUTH_FAILED", ex.args[0])
        else:
            self.fail("should have failed")
