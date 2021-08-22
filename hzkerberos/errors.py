__all__ = ("KerberosError",)


class KerberosError(RuntimeError):
    def __init__(self, msg, code):
        self.code = code
        code_msg = ERROR_MAP.get(code, "UNKNOWN: %d" % code)
        msg = "%s: %s" % (msg, code_msg)
        super().__init__(msg)


class TokenRetrievalError(RuntimeError):
    def __init__(self, msg):
        msg = "Error retrieving a token: %s" % msg
        super().__init__(msg)


ERROR_MAP = {
    -1765328189: "KRB5_FCC_NOFILE",
    -1765328203: "KRB5_KT_NOTFOUND",
    -1765328228: "KRB5_KDC_UNREACH",
    -1765328230: "KRB5_REALM_UNKNOWN",
    -1765328360: "KRB5KDC_ERR_PREAUTH_FAILED",
    -1765328378: "KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN",
}
