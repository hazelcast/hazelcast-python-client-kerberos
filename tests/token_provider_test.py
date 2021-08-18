import unittest

from hzkerberos import TokenProvider


class TokenProviderTestCase(unittest.TestCase):
    def test_spn_required(self):
        self.assertRaises(ValueError, lambda: TokenProvider(""))
        self.assertRaises(ValueError, lambda: TokenProvider(None))

    def test_password_keytab(self):
        self.assertRaises(ValueError, lambda: TokenProvider("spn", password="a", keytab="b"))
