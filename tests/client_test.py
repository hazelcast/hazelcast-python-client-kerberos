import logging
import unittest

import hazelcast

import hzkerberos
from .util import default_keytab, Address


def customize_logger(name):
    lg = logging.getLogger(name)
    lg.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    lg.addHandler(handler)


customize_logger("hazelcast")
customize_logger("hzkerberos")


class ClientTest(unittest.TestCase):
    default_address = None

    @classmethod
    def setUpClass(cls):
        cls.default_address = Address(host="hz1", resolve=True)

    def test_token(self):
        token_provider = hzkerberos.TokenProvider(keytab=default_keytab())
        addr = "%s:5701" % self.default_address.host
        client = hazelcast.HazelcastClient(
            cluster_members=[addr],
            token_provider=token_provider,
            cluster_connect_timeout=5,
        )
        m = client.get_map("auth-map").blocking()
        m.put("k1", "v1")
        v = m.get("k1")
        self.assertEqual("v1", v)
