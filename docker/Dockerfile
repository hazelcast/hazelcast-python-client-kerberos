FROM debian:stretch

LABEL maintainer="Hazelcast Engineering <>"

ARG KERBEROS_PASSWORD=Password01
ARG HAZELCAST_ENTERPRISE_KEY=""

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
COPY etc/apt/apt.conf.d/02nocache /etc/apt/apt.conf.d/02nocache
COPY etc/dpkg/dpkg.cfg.d/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

COPY create_conf.sh /root

RUN \
  bash /root/create_conf.sh

RUN \
    chown -R hz:hz $HOME && \
    apt-get update && \
    apt-get install -y --no-install-recommends openjdk-8-jdk-headless && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        libreadline7 \
        libssl1.1 \
        zlib1g \
        krb5-user krb5-kdc krb5-admin-server krb5-multidev \
        libkrb5-dev \
        python3-dev python3-venv \
        vim \
        build-essential \
        maven \
        git \
        && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr/share/doc -depth -type f ! -name copyright|xargs rm || true && \
    find /usr/share/doc -empty|xargs rmdir || true && \
    rm -rf /usr/share/man/* /usr/share/info/* rm -rf /usr/share/lintian/* && \
    rm -rf /usr/share/groff/* /usr/share/linda/* /var/cache/man/*


COPY entrypoint.sh /root/entrypoint.sh

RUN \
   chmod +x /root/entrypoint.sh && \
   printf "${KERBEROS_PASSWORD}\n${KERBEROS_PASSWORD}" | krb5_newrealm && \
   kadmin.local -q "addprinc -pw ${KERBEROS_PASSWORD} admin"

USER hz

COPY rc.sh $HOME/rc.sh
COPY requirements-test.txt $HOME/requirements-test.txt
COPY requirements.txt $HOME/requirements.txt

RUN \
    python3 -m venv venv && \
    $HOME/venv/bin/pip3 install wheel && \
    $HOME/venv/bin/pip3 install gssapi && \
    $HOME/venv/bin/pip3 install -r $HOME/requirements-test.txt &&\
    $HOME/venv/bin/pip3 install -r $HOME/requirements.txt

# starting and stopping the client to download cluster artifacts
RUN \
  bash $HOME/rc.sh start && \
  bash $HOME/rc.sh stop

USER root

ENTRYPOINT ["/root/entrypoint.sh"]
