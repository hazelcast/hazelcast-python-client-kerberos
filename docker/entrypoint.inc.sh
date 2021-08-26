# Exit immediately on error.
set -e
# Treat unset variables an parameters as an error.
set -u

TIMESTAMP_FMT="+%Y-%m-%d %H:%M:%S"

verbose=${VERBOSE:-}

if [ "$verbose" == "1" ]; then
  # Enable printing trace.
  set -x
fi

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

host=${HOSTNAME}
# get the IP and trim it
ip=$(hostname -I | xargs)
cmd=${1:-}

log_info "Host     = $host"
log_info "IP       = $ip"
log_info "Cmd      = $cmd"
