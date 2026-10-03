import secrets
import string

_ALPHABET = string.ascii_letters + string.digits
_SHORT_CODE_LENGTH = 6


def generate_short_code() -> str:
    return "".join(
        secrets.choice(_ALPHABET)
        for _ in range(_SHORT_CODE_LENGTH)
    )
