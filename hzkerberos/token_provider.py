from .c import Krb5


class TokenProvider(object):

    def __init__(self, spn="", username="", password="", realm="", libname="libkrb5.so"):
        self.spn = spn
        self.username = username
        self.password = password
        self.realm = realm
        self.__krb5 = Krb5(libname=libname)

    def token(self):
        # type: () -> bytes
        princname = self.spn if self.spn else "%s@%s" % (self.username, self.realm.upper())
        return self.__krb5.get_token(princname, self.password)
