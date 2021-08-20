#! /bin/bash

set -e
set -u

run_test () {
  sleep 1
  # assumes /app is the project root
  su -s /bin/bash hz -c "
    bash rc.sh start
    sleep 5
    source venv/bin/activate
    cd ~/app
    make test-all
  "
}

principal="hz/${HOSTNAME}@EXAMPLE.COM"
principalpw="hz1/${HOSTNAME}@EXAMPLE.COM"

echo "$(hostname -I) example.com" >> /etc/hosts
echo "$(hostname -I) ${HOSTNAME}.example.com" >> /etc/hosts

kadmin.local -q "addprinc -randkey $principal" && \
kadmin.local -q "addprinc -pw Password01 $principalpw" && \
kadmin.local -q "ktadd -k /etc/krb5.keytab $principal" && \
chmod 777 /etc/krb5.keytab

service krb5-kdc restart

cmd=${1:-}

echo "CMD: $cmd"

case "$cmd" in
  "")
  /bin/bash
  ;;

  "test")
  run_test
  ;;

  "*")
  /bin/bash -c "$@"
  ;;
esac
