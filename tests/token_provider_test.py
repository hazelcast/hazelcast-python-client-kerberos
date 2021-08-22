import unittest

from hzkerberos import TokenProvider


class TokenProviderTestCase(unittest.TestCase):
    def test_password_keytab(self):
        self.assertRaises(ValueError, lambda: TokenProvider("principal", password="a", keytab="b"))
