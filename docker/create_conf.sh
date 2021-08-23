#! /bin/bash

set -e
set -u

domain=${1:-example.com}
kdc=${2:-kdc}
realm=${domain^^}

cat > /etc/krb5.conf <<EOL
[libdefaults]
    default_realm = ${realm}
    dns_lookup_realm = false
    dns_lookup_kdc = false

[realms]
    ${realm} = {
        kdc = ${kdc}
        admin_server = ${kdc}
    }

[domain_realm]
    .${domain} = ${realm}

[logging]
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmin.log
    default = FILE:/var/log/krb5lib.log
EOL

mkdir -p /etc/krb5kdc
cat > /etc/krb5kdc/kadm5.acl <<EOL
admin *
EOL
