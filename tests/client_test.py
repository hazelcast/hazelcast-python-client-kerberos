import unittest

import hazelcast

import hzkerberos
from .util import default_keytab, Address


class ClientTest(unittest.TestCase):
    default_address = None

    @classmethod
    def setUpClass(cls):
        cls.default_address = Address(host="hz1", resolve=True)

    def test_token(self):
        token_provider = hzkerberos.TokenProvider(keytab=default_keytab())
        addr = "%s:5701" % self.default_address.host
        client = hazelcast.HazelcastClient(cluster_members=[addr], token_provider=token_provider)
        m = client.get_map("auth-map").blocking()
        m.put("k1", "v1")
        v = m.get("k1")
        self.assertEqual("v1", v)
