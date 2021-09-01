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

run_coverage () {
  # assumes /app is the project root
  su -s /bin/bash hz -c "
    source venv/bin/activate
    cd ~/app
    make test-cover
  "
}

run_package () {
  # assumes /app is the project root
  su -s /bin/bash hz -c "
    source venv/bin/activate
    pip install -U pip
    pip install -U setuptools
    cd /home/hz/app
    ls -l
    make package
  "
}

case "$cmd" in
  "/bin/bash")
  su -s /bin/bash hz
  ;;

  "test")
  run_test
  ;;

  "coverage")
  run_coverage
  ;;

  "package")
  run_package
  ;;

  "*")
  /bin/bash -c "$@"
  ;;
esac
