import socket


def make_principal(prefix="hz", fqdn="", realm="example.com"):
    hostname = fqdn or socket.gethostname()
    realm = realm.upper()
    return "%s/%s@%s" % (prefix, hostname, realm)


def default_keytab():
    return "/etc/krb5.keytab"
