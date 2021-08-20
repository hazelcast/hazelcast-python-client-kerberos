import unittest

import hazelcast

import hzkerberos
from tests.hzrc.client import HzRemoteController
from .util import make_principal, default_keytab


class Krb5TestCase(unittest.TestCase):
    rc = None

    @classmethod
    def create_cluster(cls, config):
        cluster = cls.rc.createCluster("4.2.1", config)
        cls.rc.startMember(cluster.id)
        return cluster

    @classmethod
    def setUpClass(cls):
        cls.rc = HzRemoteController("127.0.0.1", 9701)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.rc.exit()

    def test_token(self):
        principal = make_principal()
        keytab = default_keytab()
        cluster = self.create_cluster(xml_config(principal, keytab))
        token_provider = hzkerberos.TokenProvider(principal=principal, keytab=keytab)
        client = hazelcast.HazelcastClient(cluster_name=cluster.id, token_provider=token_provider)
        m = client.get_map("auth-map").blocking()
        m.put("k1", "v1")
        v = m.get("k1")
        self.assertEqual("v1", v)


def xml_config(principal, keytab):
    return """
        <hazelcast xmlns="http://www.hazelcast.com/schema/config"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.hazelcast.com/schema/config
            http://www.hazelcast.com/schema/config/hazelcast-config-4.2.xsd"
        >
            <security enabled="true">
                <client-authentication realm="kerberosRealm"/>
                <client-permissions>
                    <map-permission name="auth-map" principal="*">
                        <actions>
                            <action>create</action>
                            <action>destroy</action>
                            <action>put</action>
                            <action>read</action>
                        </actions>
                    </map-permission>
                </client-permissions>
                <realms>
                    <realm name="krb5Acceptor">
                        <authentication>
                            <jaas>
                                <login-module class-name="com.sun.security.auth.module.Krb5LoginModule" usage="REQUIRED">
                                    <properties>
                                        <property name="isInitiator">false</property>
                                        <property name="useTicketCache">false</property>
                                        <property name="doNotPrompt">true</property>
                                        <property name="useKeyTab">true</property>
                                        <property name="storeKey">true</property>
                                        <property name="principal">{principal}</property>
                                        <property name="keyTab">{keytab}</property>
                                    </properties>
                                </login-module>
                            </jaas>
                        </authentication>
                    </realm>
                    <realm name="kerberosRealm">
                        <authentication>
                            <kerberos>
                                <relax-flags-check>true</relax-flags-check>
                                <use-name-without-realm>false</use-name-without-realm>
                                <security-realm>krb5Acceptor</security-realm>
                            </kerberos>
                        </authentication>
                    </realm>
                </realms>
            </security>            
        </hazelcast>        
    """.format(
        principal=principal, keytab=keytab
    )
