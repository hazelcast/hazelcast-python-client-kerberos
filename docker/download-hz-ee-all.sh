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
HZ_VERSION=${HZ_VERSION:-4.2.2}
LOG4J2_VERSION=${LOG4J2_VERSION:-2.14.1}

log_info () {
  local msg=${1:-}
  local ts
  ts=$(date "$TIMESTAMP_FMT")
  echo "$ts INFO : $msg"
}

download_jar () {
  local repo=$1
  local jar_path=$2
  local artifact=$3
  if [ -f "$jar_path" ]; then
      log_info "$jar_path already exists, skipping download."
  else
      log_info "Downloading: $jar_path ($artifact) from: $repo"
      mvn -q dependency:get -DrepoUrl=$repo -Dartifact=$artifact -Ddest="$jar_path" -Dtransitive=false
      if [ $? -ne 0 ]; then
          log_fatal "Failed downloading $jar_path ($artifact) from: $repo"
      fi
  fi
}

download_hz_ee () {
  local jar_path="hazelcast-enterprise-${HZ_VERSION}.jar"
  local artifact="com.hazelcast:hazelcast-enterprise:${HZ_VERSION}"
  download_jar "https://repository.hazelcast.com/release/" "$jar_path" "$artifact"
}

download_lj2 () {
  local jar_path="log4j-core/${LOG4J2_VERSION}.jar"
  local artifact="org.apache.logging.log4j:log4j-core:${LOG4J2_VERSION}"
  download_jar "https://repo1.maven.org/maven2/" "$jar_path" "$artifact"

  local jar_path="log4j-api/${LOG4J2_VERSION}.jar"
  local artifact="org.apache.logging.log4j:log4j-api:${LOG4J2_VERSION}"
  download_jar "https://repo1.maven.org/maven2/" "$jar_path" "$artifact"

}

download_lj2
download_hz_ee
