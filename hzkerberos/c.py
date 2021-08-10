from ctypes import Structure, POINTER
from ctypes import c_char, c_char_p, c_int32, c_uint, c_uint8, c_void_p, c_size_t
from ctypes import cdll, byref, memmove


class KerberosError(RuntimeError):

    def __init__(self, code):
        self.code = code
        msg = ERROR_MAP.get(code, "UNKNOWN: %d" % code)
        super().__init__(msg)


krb5_int32 = c_int32
krb5_flags = c_int32
krb5_addrtype = c_int32
krb5_authtype = c_int32
krb5_deltat = c_int32
krb5_boolean = c_uint
krb5_error_code = krb5_int32
krb5_enctype = krb5_int32
krb5_timestamp = krb5_int32
krb5_magic = krb5_error_code
krb5_octet = c_uint8


class Krb5Data(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("length", c_uint),
        ("data", c_void_p),
    ]


class Krb5PrincipalData(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("realm", Krb5Data),
        ("data", POINTER(Krb5Data)),
        ("length", krb5_int32),
        ("type", krb5_int32),
    ]


krb5_principal = POINTER(Krb5PrincipalData)


class Krb5KeyBlock(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("enctype", krb5_enctype),
        ("length", c_uint),
        ("content", POINTER(krb5_octet)),
    ]


class Krb5TicketTimes(Structure):
    _fields_ = [
        ("authtime", krb5_timestamp),
        ("starttime", krb5_timestamp),
        ("endtime", krb5_timestamp),
        ("renew_till", krb5_timestamp),
    ]


class Krb5Address(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("addrtype", krb5_addrtype),
        ("length", c_uint),
        ("contents", POINTER(krb5_octet)),
    ]


class Krb5AuthData(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("authtype", krb5_authtype),
        ("length", c_uint),
        ("contents", POINTER(krb5_octet)),
    ]


class Krb5Creds(Structure):
    _fields_ = [
        ("magic", krb5_magic),
        ("client", krb5_principal),
        ("server", krb5_principal),
        ("keyblock", Krb5KeyBlock),
        ("times", Krb5TicketTimes),
        ("is_skey", krb5_boolean),
        ("ticket_flags", krb5_flags),
        ("addresses", POINTER(POINTER(Krb5Address))),
        ("ticket", Krb5Data),
        ("second_ticket", Krb5Data),
        ("authdata", POINTER(POINTER(Krb5AuthData)))
    ]


class Krb5Context(Structure):
    pass


krb5_context = POINTER(Krb5Context)


class Krb5(object):
    lib = None
    parse_name = None
    get_init_creds_password = None
    free_principal = None
    free_cred_contents = None
    init_context = None
    free_context = None
    memcpy = None

    def __init__(self, libname="libkrb5.so"):
        if Krb5.lib is None:
            lib = cdll.LoadLibrary(libname)
            Krb5.lib = lib

            f = lib.krb5_parse_name
            f.argtypes = (krb5_context, c_char_p, POINTER(krb5_principal))
            f.restype = krb5_error_code
            Krb5.parse_name = f

            f = lib.krb5_get_init_creds_password
            f.argtypes = (
            krb5_context, POINTER(Krb5Creds), krb5_principal, c_char_p, c_void_p, c_void_p, krb5_deltat, c_char_p,
            c_void_p)
            f.restype = krb5_error_code
            Krb5.get_init_creds_password = f

            f = lib.krb5_free_principal
            f.argtypes = (krb5_context, krb5_principal)
            f.restype = None
            Krb5.free_principal = f

            f = lib.krb5_free_cred_contents
            f.argtypes = (krb5_context, POINTER(Krb5Creds))
            f.restype = None
            Krb5.free_cred_contents = f

            f = lib.krb5_init_context
            f.argtypes = (POINTER(krb5_context),)
            f.restype = krb5_error_code
            Krb5.init_context = f

            f = lib.krb5_free_context
            f.argtypes = (krb5_context,)
            f.restype = None
            Krb5.free_context = f

            clib = cdll.LoadLibrary("libc.so.6")

            f = clib.memcpy
            f.argtypes = (c_void_p, c_void_p, c_size_t)
            f.restype = c_void_p
            Krb5.memcpy = f

    def get_token(self, princname, password):
        # type: (Krb5, str, str) -> bytes

        def cleanup():
            self.free_principal(context, client_princ)
            self.free_cred_contents(context, byref(creds))
            self.free_context(context)

        context = krb5_context()
        self.init_context(byref(context))
        creds = Krb5Creds()
        client_princ = krb5_principal()
        ret = self.parse_name(context, princname.encode("utf-8"), byref(client_princ))
        if ret:
            cleanup()
            raise KerberosError(code=ret)
        ret = self.get_init_creds_password(context, byref(creds), client_princ, password.encode("utf-8"), 0, None, 0,
                                           None, 0)
        if ret:
            cleanup()
            raise KerberosError(code=ret)
        ticket_len = creds.ticket.length
        if ticket_len < 0:
            raise RuntimeError("illegal ticket length")
        ticket = (c_char * ticket_len)()
        memmove(ticket, creds.ticket.data, ticket_len)
        cleanup()
        return memoryview(ticket).tobytes()


ERROR_MAP = {
    -1765328228: "KRB5_KDC_UNREACH",
    -1765328230: "KRB5_REALM_UNKNOWN",
}
