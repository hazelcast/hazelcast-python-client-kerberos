import logging

from .errors import KerberosError
from .token_provider import TokenProvider

logging.getLogger("hzkerberos").addHandler(logging.NullHandler())
