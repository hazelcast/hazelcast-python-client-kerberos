import logging

from .errors import KerberosError, TokenRetrievalError
from .token_provider import TokenProvider

logging.getLogger("hzkerberos").addHandler(logging.NullHandler())
