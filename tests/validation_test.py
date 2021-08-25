import unittest

from hzkerberos.token_provider import _make_principal


class ValidationTest(unittest.TestCase):

    def test_make_principal(self):
        table = [
            # target, input
            ("hz/1.2.3.4", lambda: _make_principal("1.2.3.4")),
            ("HTTP/1.2.3.4", lambda: _make_principal("1.2.3.4", prefix="HTTP/")),
            ("HTTP/1.2.3.4", lambda: _make_principal("1.2.3.4", prefix="HTTP")),
            ("1.2.3.4", lambda: _make_principal("1.2.3.4", prefix="")),
            ("hz/1.2.3.4@EXAMPLE.COM", lambda: _make_principal("1.2.3.4", realm="example.com")),
            ("hz/1.2.3.4@EXAMPLE.COM", lambda: _make_principal("1.2.3.4@EXAMPLE.COM", realm="example.com")),
        ]
        for target, input in table:
            self.assertEqual(target, input())
