FROM debian:buster

LABEL maintainer="Hazelcast Engineering <info@hazelcast.com>"

ARG HAZELCAST_ENTERPRISE_KEY=""
ARG HZ_VERSION=4.2.2

# Create the default users and groups.
RUN \
  addgroup --gid 1000 hz && \
  useradd --shell /bin/false --uid 1000 --gid 1000 hz

ENV \
  HOME=/home/hz \
  LANG=C.UTF-8 \
  DEBIAN_FRONTEND=noninteractive

WORKDIR $HOME

# Make sure documentation is not cached.
COPY docker/etc/apt/apt.conf.d/02nocache /etc/apt/apt.conf.d/02nocache
COPY docker/etc/dpkg/dpkg.cfg.d/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

COPY docker/create_conf.sh /root

RUN \
  bash /root/create_conf.sh

RUN \
  chown -R hz:hz $HOME && \
  apt-get update && \
  apt-get install -y --no-install-recommends openjdk-11-jdk-headless && \
  apt-get install -y --no-install-recommends \
    ca-certificates \
    libreadline7 \
    libssl1.1 \
    zlib1g \
    krb5-user \
    libkrb5-dev \
    vim \
    curl \
    rlwrap \
    maven \
    && \
  rm -rf /var/lib/apt/lists/* && \
  find /usr/share/doc -depth -type f ! -name copyright|xargs rm || true && \
  find /usr/share/doc -empty|xargs rmdir || true && \
  rm -rf /usr/share/man/* /usr/share/info/* rm -rf /usr/share/lintian/* && \
  rm -rf /usr/share/groff/* /usr/share/linda/* /var/cache/man/*

USER hz

RUN mkdir $HOME/lib

COPY docker/log4j2.properties $HOME/
COPY docker/start-hz.sh $HOME/

USER root

COPY docker/download-hz-ee-all.sh /$HOME/

RUN \
  cd $HOME/lib &&\
  bash $HOME/download-hz-ee-all.sh

COPY docker/hz-entrypoint.sh /root/
COPY docker/entrypoint.inc.sh /root/

RUN \
  chown -R hz:hz $HOME && \
  chmod +x $HOME/start-hz.sh && \
  chmod +x /root/hz-entrypoint.sh

ENTRYPOINT ["/root/hz-entrypoint.sh"]
CMD ["run"]
