#! /bin/bash

source /root/entrypoint.inc.sh

run_test () {
  # assumes /app is the project root
  su -s /bin/bash hz -c "
    source venv/bin/activate
    cd ~/app
    make test-all
  "
}

case "$cmd" in
  "/bin/bash")
  su -s /bin/bash hz
  ;;

  "test")
  run_test
  ;;

  "*")
  /bin/bash -c "$@"
  ;;
esac
