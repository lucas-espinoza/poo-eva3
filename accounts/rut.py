import re
from django.core.exceptions import ValidationError

RUT_RE = re.compile(r"^(\d{1,8})-([0-9Kk])$")
def validate_rut(value):
    match = RUT_RE.fullmatch(value or "")
    if not match:
        raise ValidationError("Ingrese un RUT válido.")
    digits, check = match.groups()
    total, factor = 0, 2
    for digit in reversed(digits):
        total += int(digit) * factor; factor = factor + 1 if factor < 7 else 2
    remainder = 11 - (total % 11)
    expected = "0" if remainder == 11 else "K" if remainder == 10 else str(remainder)
    if check.upper() != expected:
        raise ValidationError("Ingrese un RUT válido.")
