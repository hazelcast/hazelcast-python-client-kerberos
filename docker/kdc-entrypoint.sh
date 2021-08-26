#! /bin/bash

source /root/entrypoint.inc.sh

keytab="/common/krb5.keytab"

add_principal () {
  local princ=${1:-}
  local pass=${2:-}

  if [ "x$princ" == "x" ]; then
    log_fatal "add_principal: principal is required"
  fi
  if [ "x${pass}" == "x" ]; then
    log_info "add_principal: $princ without a password"
    kadmin.local -q "addprinc -randkey $princ"
    kadmin.local -q "ktadd -k $keytab $princ"
  else
    log_info "add_principal: $princ with password: $pass"
    kadmin.local -q "addprinc -pw $pass $princ"
  fi
}

add_principals () {
  # delete the keytab, for clean state
  rm -f $keytab
  # create default credentials
  add_principal "jduke@EXAMPLE.COM" "p1"
  add_principal "jkey@EXAMPLE.COM"
  # create given credentials
  shift
  for host in "$@"; do
    local ip
    for i in {1..10}; do
      log_info "Getting IP for host: $host (attempt: $i)"
      ip=$(getent hosts $host | awk '{print $1}')
      if [ "x$ip" == "x" ]; then
        sleep 1
      else
        local p="hz/${ip}@EXAMPLE.COM"
        add_principal $p
        break
      fi
    done
  done
  chmod 777 $keytab
  service krb5-kdc restart
  service krb5-admin-server start
  /usr/sbin/kadmin.local
}

domain="example.com"
# realm is upper case
realm=${domain^^}

log_info "Realm    = $realm"
log_info "Keytab   = $keytab"
log_info

case "$cmd" in
  "/bin/bash")
  /bin/bash
  ;;

  "add_principals")
  add_principals "$@"
  ;;

  "*")
  /bin/bash -c "$@"
  ;;
esac
