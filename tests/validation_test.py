import unittest

from hzkerberos.token_provider import _make_spn, TokenProvider


class ValidationTest(unittest.TestCase):

    def test_make_spn(self):
        table = [
            # target, input
            ("hz/1.2.3.4", lambda: _make_spn("1.2.3.4")),
            ("HTTP/1.2.3.4", lambda: _make_spn("1.2.3.4", prefix="HTTP/")),
            ("HTTP/1.2.3.4", lambda: _make_spn("1.2.3.4", prefix="HTTP")),
            ("1.2.3.4", lambda: _make_spn("1.2.3.4", prefix="")),
            ("hz/1.2.3.4@EXAMPLE.COM", lambda: _make_spn("1.2.3.4", realm="example.com")),
            ("hz/1.2.3.4@EXAMPLE.COM", lambda: _make_spn("1.2.3.4@EXAMPLE.COM", realm="example.com")),
        ]
        for target, input in table:
            self.assertEqual(target, input())

    def test_principal_required(self):
        TokenProvider(principal="foo", password="123")
        TokenProvider(principal="foo", keytab="krb5.keytab")
        self.assertRaisesRegex(ValueError,
                               "keytab or password is required when the principal is specified",
                               lambda: TokenProvider(principal="foo"))

    def test_principal_with_both_password_keytab(self):
        self.assertRaisesRegex(ValueError,
                               "keytab and password are mutually exclusive",
                               lambda: TokenProvider(principal="foo", password="123", keytab="krb5.keytab"))
