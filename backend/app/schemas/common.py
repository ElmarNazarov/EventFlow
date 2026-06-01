import re
from typing import Annotated

from pydantic import AfterValidator

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(value: str) -> str:
    normalized = value.lower().strip()
    if not _EMAIL_PATTERN.match(normalized):
        raise ValueError("Invalid email address")
    return normalized


EmailStrLocal = Annotated[str, AfterValidator(_validate_email)]
