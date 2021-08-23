FROM debian:stretch

LABEL maintainer="Hazelcast Engineering <info@hazelcast.com>"

ARG KERBEROS_PASSWORD=p1

EXPOSE 88
EXPOSE 88/udp
EXPOSE 749
EXPOSE 749/udp

ENV \
  HOME=/root \
  LANG=C.UTF-8 \
  DEBIAN_FRONTEND=noninteractive

WORKDIR $HOME

# Make sure documentation is not cached.
COPY docker/etc/apt/apt.conf.d/02nocache /etc/apt/apt.conf.d/02nocache
COPY docker/etc/dpkg/dpkg.cfg.d/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

COPY docker/create_conf.sh /root/

RUN \
  bash /root/create_conf.sh && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    libreadline7 \
    krb5-user krb5-kdc krb5-admin-server krb5-multidev \
    vim \
    rlwrap \
    && \
  rm -rf /var/lib/apt/lists/* && \
  find /usr/share/doc -depth -type f ! -name copyright|xargs rm || true && \
  find /usr/share/doc -empty|xargs rmdir || true && \
  rm -rf /usr/share/man/* /usr/share/info/* rm -rf /usr/share/lintian/* && \
  rm -rf /usr/share/groff/* /usr/share/linda/* /var/cache/man/*

COPY docker/kdc-entrypoint.sh /root/kdc-entrypoint.sh
COPY docker/entrypoint.inc.sh /root/

RUN \
  printf "${KERBEROS_PASSWORD}\n${KERBEROS_PASSWORD}" | krb5_newrealm && \
  kadmin.local -q "addprinc -pw ${KERBEROS_PASSWORD} admin" && \
  chmod +x /root/kdc-entrypoint.sh

ENTRYPOINT ["/root/kdc-entrypoint.sh"]
CMD ["add_principals", "hz1", "hz2"]
