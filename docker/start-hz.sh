#! /bin/bash

set -e
set -u

if [ "x${LOGGING_LEVEL:-}" == "x" ]; then
  export LOGGING_LEVEL="INFO"
fi

export LOGGING_PATTERN="%d [%highlight{\${LOG_LEVEL_PATTERN:-%5p}}{FATAL=red, ERROR=red, WARN=yellow, INFO=green, DEBUG=magenta}] [%style{%t{1.}}{cyan}] [%style{%c{1.}}{blue}]: %m%n"

cp="lib/hazelcast-enterprise-4.2.2.jar:lib/log4j-api/2.14.1.jar:lib/log4j-core/2.14.1.jar"
opts="
-Dhazelcast.phone.home.enabled=false \
-Dhazelcast.config=/home/hz/hazelcast.xml \
-Dhazelcast.logging.type=log4j2 \
-Dsun.security.krb5.debug=true \
-Djava.net.preferIPv4Stack=true \
-Dlog4j.configurationFile=${HOME}/log4j2.properties \
-XX:MaxRAMPercentage=80.0 \
-XX:MaxGCPauseMillis=5 \
--add-modules java.se \
--add-exports java.base/jdk.internal.ref=ALL-UNNAMED \
--add-opens java.base/java.lang=ALL-UNNAMED \
--add-opens java.base/java.nio=ALL-UNNAMED \
--add-opens java.base/sun.nio.ch=ALL-UNNAMED \
--add-opens java.management/sun.management=ALL-UNNAMED \
--add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED \
"
set -x
java -cp "$cp" -server $opts  com.hazelcast.core.server.HazelcastMemberStarter
set +x