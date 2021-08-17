#! /bin/bash

set -e
set -u

domain=${1:-example.com}
kerberos_realm=${domain^^}
kerberos_domain=${domain}

cat > /etc/krb5.conf << EOL
[libdefaults]
    default_realm = ${kerberos_realm}
    dns_lookup_realm = false
    dns_lookup_kdc = false

[realms]
    ${kerberos_realm} = {
        kdc = ${kerberos_domain}
        admin_server = ${kerberos_domain}
    }

[domain_realm]
    .${domain} = ${kerberos_realm}

[logging]
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmin.log
    default = FILE:/var/log/krb5lib.log
EOL
