import socket


def make_principal(prefix="hz/", host="", realm="example.com"):
    realm = realm.upper()
    return "%s%s@%s" % (prefix, host, realm)


def default_keytab():
    return "/common/krb5.keytab"


class Address:
    def __init__(self, host="", resolve=False):
        if host and resolve:
            self.host = Address._resolve_host(host)
        else:
            self.host = host or self._get_current_ip()

    @classmethod
    def _get_current_ip(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    @classmethod
    def _resolve_host(cls, host):
        return socket.gethostbyname(host)
