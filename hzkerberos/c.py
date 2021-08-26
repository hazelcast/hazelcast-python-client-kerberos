from ctypes import Structure, POINTER
from ctypes import c_char_p, c_int32, c_uint, c_uint8, c_void_p, c_int
from ctypes import cdll, byref, cast, pointer

import gssapi

from .errors import KerberosError

krb5_int32 = c_int32
krb5_flags = c_int32
krb5_addrtype = c_int32
krb5_authtype = c_int32
krb5_deltat = c_int32
krb5_boolean = c_uint
krb5_error_code = krb5_int32
krb5_enctype = krb5_int32
krb5_timestamp = krb5_int32
krb5_preauthtype = krb5_int32
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
        ("authdata", POINTER(POINTER(Krb5AuthData))),
    ]


class Krb5GetInitCredsOpt(Structure):
    _fields_ = [
        ("flags", krb5_flags),
        ("tkt_life", krb5_deltat),
        ("renew_life", krb5_deltat),
        ("forwardable", c_int),
        ("proxiable", c_int),
        ("etype_list", POINTER(krb5_enctype)),
        ("etype_list_length", c_int),
        ("address_list", POINTER(POINTER(Krb5Address))),
        ("preauth_list", POINTER(krb5_preauthtype)),
        ("preauth_list_length", c_int),
        ("salt", POINTER(Krb5Data)),
    ]


class Krb5Context(Structure):
    pass


class Krb5KeyTab(Structure):
    pass


class Krb5InitCredsContext(Structure):
    pass


class Krb5CCache(Structure):
    pass


krb5_context = POINTER(Krb5Context)
krb5_keytab = POINTER(Krb5KeyTab)
krb5_init_creds_context = POINTER(Krb5InitCredsContext)
krb5_ccache = POINTER(Krb5CCache)


class Krb5(object):
    lib = None
    cc_close = None
    cc_default_name = None
    cc_destroy = None
    cc_resolve = None
    free_context = None
    free_cred_contents = None
    free_error_message = None
    free_principal = None
    get_error_message = None
    get_init_creds_keytab = None
    get_init_creds_opt_alloc = None
    get_init_creds_opt_free = None
    get_init_creds_opt_set_out_ccache = None
    get_init_creds_password = None
    init_context = None
    kt_close = None
    kt_resolve = None
    parse_name = None

    def __init__(self, libname="libkrb5.so"):
        if Krb5.lib is None and libname:
            try:
                lib = cdll.LoadLibrary(libname)
            except OSError:
                return
            Krb5.lib = lib

            f = lib.krb5_parse_name
            f.argtypes = (krb5_context, c_char_p, POINTER(krb5_principal))
            f.restype = krb5_error_code
            Krb5.parse_name = f

            f = lib.krb5_get_init_creds_password
            f.argtypes = (
                krb5_context,
                POINTER(Krb5Creds),
                krb5_principal,
                c_char_p,
                c_void_p,
                c_void_p,
                krb5_deltat,
                c_char_p,
                c_void_p,
            )
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

            f = lib.krb5_get_error_message
            f.argtypes = (krb5_context, krb5_error_code)
            f.restype = c_void_p
            Krb5.get_error_message = f

            f = lib.krb5_free_error_message
            f.argtypes = (krb5_context, c_char_p)
            f.restype = None
            Krb5.free_error_message = f

            f = lib.krb5_kt_resolve
            f.argtypes = (krb5_context, c_char_p, POINTER(krb5_keytab))
            f.restype = krb5_error_code
            Krb5.kt_resolve = f

            f = lib.krb5_kt_close
            f.argtypes = (krb5_context, krb5_keytab)
            f.restype = krb5_error_code
            Krb5.kt_close = f

            f = lib.krb5_get_init_creds_keytab
            f.argtypes = (
                krb5_context,
                POINTER(Krb5Creds),
                krb5_principal,
                krb5_keytab,
                krb5_deltat,
                c_char_p,
                c_void_p,
            )
            f.restype = krb5_error_code
            Krb5.get_init_creds_keytab = f

            f = lib.krb5_get_init_creds_opt_alloc
            f.argtypes = (krb5_context, POINTER(POINTER(Krb5GetInitCredsOpt)))
            f.restype = krb5_error_code
            Krb5.get_init_creds_opt_alloc = f

            f = lib.krb5_get_init_creds_opt_set_out_ccache
            f.argtypes = (krb5_context, POINTER(Krb5GetInitCredsOpt), krb5_ccache)
            f.restype = krb5_error_code
            Krb5.get_init_creds_opt_set_out_ccache = f

            f = lib.krb5_get_init_creds_opt_free
            f.argtypes = (krb5_context, POINTER(Krb5GetInitCredsOpt))
            f.restype = krb5_error_code
            Krb5.get_init_creds_opt_free = f

            f = lib.krb5_cc_default_name
            f.argtypes = (krb5_context,)
            f.restype = c_char_p
            Krb5.cc_default_name = f

            f = lib.krb5_cc_resolve
            f.argtypes = (krb5_context, c_char_p, POINTER(krb5_ccache))
            f.restype = krb5_error_code
            Krb5.cc_resolve = f

            f = lib.krb5_cc_close
            f.argtypes = (krb5_context, krb5_ccache)
            f.restype = krb5_error_code
            Krb5.cc_close = f

            f = lib.krb5_cc_destroy
            f.argtypes = (krb5_context, krb5_ccache)
            f.restype = krb5_error_code
            Krb5.cc_destroy = f

    @classmethod
    def get_token(cls, principal="", spn="", password="", keytab=""):
        # type: (Krb5, str, str, str, str) -> bytes

        if cls.lib and (password or keytab):
            cls._cache_credentials(principal, password, keytab)
        server_name = gssapi.Name(spn)
        client_ctx = gssapi.SecurityContext(name=server_name, usage="initiate")
        token = client_ctx.step()
        return token

    @classmethod
    def _cache_credentials(cls, principal, password, keytab):
        # authenticates the principal by using a password or the keytab and caches the credentials.

        def cleanup():
            if keytab_handle:
                cls.kt_close(context, keytab_handle)
            cls.free_principal(context, client_princ)
            cls.free_cred_contents(context, byref(creds))
            cls.get_init_creds_opt_free(context, optp)
            cls.cc_close(context, cache)
            cls.free_context(context)

        def ok(ret):
            if ret:
                cleanup()
                raise KerberosError(msg=cls._make_error_msg(context, ret), code=ret)

        keytab_handle = None
        context = krb5_context()
        cls.init_context(byref(context))
        creds = Krb5Creds()
        client_princ = krb5_principal()
        ok(cls.parse_name(context, principal.encode("utf-8"), byref(client_princ)))

        # initialize credentials options
        opt = Krb5GetInitCredsOpt()
        optp = pointer(opt)
        ok(cls.get_init_creds_opt_alloc(context, byref(optp)))

        # set the credentials cache
        cache_name = cls.cc_default_name(context)
        cache = krb5_ccache()
        ok(cls.cc_resolve(context, cache_name, byref(cache)))
        ok(cls.get_init_creds_opt_set_out_ccache(context, optp, cache))

        # authenticate
        if keytab:
            # keytab is specified, try load it
            keytab_handle = krb5_keytab()
            ret = cls.kt_resolve(context, keytab.encode("utf-8"), byref(keytab_handle))
            if not ret:
                ret = cls.get_init_creds_keytab(
                    context, byref(creds), client_princ, keytab_handle, 0, None, optp
                )
        else:
            # no keytab, try to use the password
            ret = cls.get_init_creds_password(
                context,
                byref(creds),
                client_princ,
                password.encode("utf-8"),
                None,
                None,
                0,
                None,
                optp,
            )
        ok(ret)
        cleanup()

    @classmethod
    def _destroy_cache(cls):
        def cleanup():
            # cls.cc_close(context, cache)
            cls.free_context(context)

        def ok(ret):
            if ret:
                cleanup()
                raise KerberosError(msg=cls._make_error_msg(context, ret), code=ret)

        context = krb5_context()
        cls.init_context(byref(context))

        # set the credentials cache
        cache_name = cls.cc_default_name(context)
        cache = krb5_ccache()
        ok(cls.cc_resolve(context, cache_name, byref(cache)))
        ok(cls.cc_destroy(context, cache))
        cleanup()

    @classmethod
    def _make_error_msg(cls, context, ret):
        err = cls.get_error_message(context, ret)
        err_c = cast(err, c_char_p)
        msg = err_c.value
        cls.free_error_message(context, err_c)
        return msg.decode("utf-8")
