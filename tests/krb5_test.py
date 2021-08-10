import unittest

import hzkerberos


class Krb5TestCase(unittest.TestCase):

    def test_get_token(self):
        p = hzkerberos.TokenProvider(username="administrator", password="Passw0rd1", realm="example.com")
        tok = p.token()
        self.assertIsNotNone(tok)
        self.assertIsInstance(tok, bytes)
