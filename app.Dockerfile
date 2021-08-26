FROM debian:stretch

LABEL maintainer="Hazelcast Engineering <info@hazelcast.com>"

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
  apt-get install -y --no-install-recommends \
    ca-certificates \
    libreadline7 \
    libssl1.1 \
    zlib1g \
    krb5-user \
    libkrb5-dev \
    python3-dev python3-venv \
    vim \
    build-essential \
    git \
    rlwrap \
    && \
  rm -rf /var/lib/apt/lists/* && \
  find /usr/share/doc -depth -type f ! -name copyright|xargs rm || true && \
  find /usr/share/doc -empty|xargs rmdir || true && \
  rm -rf /usr/share/man/* /usr/share/info/* rm -rf /usr/share/lintian/* && \
  rm -rf /usr/share/groff/* /usr/share/linda/* /var/cache/man/*

USER hz

COPY requirements-test.txt $HOME/
COPY requirements.txt $HOME/

RUN \
  python3 -m venv venv && \
  $HOME/venv/bin/pip3 install wheel && \
  $HOME/venv/bin/pip3 install -r $HOME/requirements-test.txt &&\
  $HOME/venv/bin/pip3 install -r $HOME/requirements.txt

USER root

COPY docker/app-entrypoint.sh /root/
COPY docker/entrypoint.inc.sh /root/

RUN chmod +x /root/app-entrypoint.sh

ENTRYPOINT ["/root/app-entrypoint.sh"]
CMD ["test"]
