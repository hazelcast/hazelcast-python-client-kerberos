#! /bin/bash

principal="hz/${HOSTNAME}@EXAMPLE.COM"

echo "$(hostname -I) example.com" >> /etc/hosts
echo "$(hostname -I) ${HOSTNAME}.example.com" >> /etc/hosts

kadmin.local -q "addprinc -randkey $principal" && \
kadmin.local -q "ktadd -k /etc/krb5.keytab $principal" && \
chmod 777 /etc/krb5.keytab

service krb5-kdc restart

su -s /bin/bash hz
