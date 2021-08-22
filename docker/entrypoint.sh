#! /bin/bash

# Exit immediately on error.
set -e
# Treat unset variables an parameters as an error.
set -u

verbose=${VERBOSE:-}

if [ "$verbose" == "1" ]; then
  # Enable printing trace.
  set -x
fi

TIMESTAMP_FMT="+%Y-%m-%d %H:%M:%S"

log_info () {
  local msg=${1:-}
  local ts
  ts=$(date "$TIMESTAMP_FMT")
  echo "$ts INFO : $msg"
}

log_fatal () {
  local msg=${1:-}
  local ts
  ts=$(date "$TIMESTAMP_FMT")
  echo "$ts FATAL: $msg"
  exit 1
}

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

add_principal () {
  local princ=${1:-}
  local pass=${2:-}

  if [ "x$princ" == "x" ]; then
    log_fatal "add_principal: principal is required"
  fi
  if [ "x${pass}" == "x" ]; then
    log_info "add_principal: $princ without a password"
    kadmin.local -q "addprinc -randkey $princ"
    kadmin.local -q "ktadd -k /etc/krb5.keytab $princ"
  else
    log_info "add_principal: $princ with password: $pass"
    kadmin.local -q "addprinc -pw $pass $princ"
  fi
}

host=${HOSTNAME}
ip=$(hostname -I)
domain="example.com"
realm=${domain^^}

log_info "Host  = $host"
log_info "IP    = $ip"
log_info "Realm = $realm"
log_info

echo "$ip $domain" >> /etc/hosts
echo "$ip $host.$domain" >> /etc/hosts

add_principal "hz/${host}@${realm}"
add_principal "hz1/${host}@${realm}" "Password01"

chmod 777 /etc/krb5.keytab
service krb5-kdc restart

cmd=${1:-}
log_info "CMD: $cmd"
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
