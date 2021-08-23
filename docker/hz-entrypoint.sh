#! /bin/bash

source /root/entrypoint.inc.sh

conf_path=/home/hz/hazelcast.xml

create_conf () {
  cat > $conf_path <<HERE
<?xml version="1.0" encoding="UTF-8"?>
<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
           http://www.hazelcast.com/schema/config/hazelcast-config-4.2.xsd">

    <cluster-name>dev</cluster-name>
    <network>
        <port auto-increment="false" port-count="100">5701</port>
        <outbound-ports>
            <ports>0</ports>
        </outbound-ports>
    </network>
    <security enabled="true">
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
        <member-authentication realm="kerberosRealm"/>
        <client-authentication realm="kerberosRealm"/>
        <realms>
            <realm name="kerberosRealm">
                <authentication>
                    <kerberos>
                        <relax-flags-check>true</relax-flags-check>
                        <use-name-without-realm>false</use-name-without-realm>
                        <keytab-file>/common/krb5.keytab</keytab-file>
                        <principal>hz/${ip}@EXAMPLE.COM</principal>
                    </kerberos>
                </authentication>
                <identity>
                    <kerberos>
                        <realm>EXAMPLE.COM</realm>
                        <keytab-file>/common/krb5.keytab</keytab-file>
                        <principal>hz/${ip}@EXAMPLE.COM</principal>
                    </kerberos>
                </identity>
            </realm>
        </realms>
    </security>
</hazelcast>
HERE
chmod 666 $conf_path
}

run () {
  log_info "Starting Hazelcast"
  su -s /bin/bash hz -c /home/hz/start-hz.sh
}

log_info "Conf     = $conf_path"
log_info

create_conf

case "$cmd" in
  "/bin/bash")
  su -s /bin/bash hz
  ;;

  "run")
  run
  ;;

  "*")
  /bin/bash -c "$@"
  ;;
esac
