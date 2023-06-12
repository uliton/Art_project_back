import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeFullnameValidator(validators.RegexValidator):
    regex = r"^[\w\s'-]+\Z"
    message = _(
        "Enter a valid full name. This value may contain only"
        "latin letters, spaces, hyphen (-), apostrophe (’)"
    )
    flags = 0


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8 or len(password) > 30:
            raise ValidationError(_("Password must be between 8 and 30 characters."))

        if not any(char.isupper() for char in password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))

        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one digit."))

        if not any(char.isalpha() for char in password):
            raise ValidationError(_("Password must contain at least one letter."))

        if not any(not char.isalnum() for char in password):
            raise ValidationError(_("Password must contain at least one special character."))

        if any(char.isprintable() for char in password):
            raise ValidationError(_("Password cannot contain non-printing symbols."))

        if password != password.strip():
            raise ValidationError(_("Password should not have leading or trailing whitespace."))

    def get_help_text(self):
        return _(
            "Your password must be between 8 and 30 characters long, "
            "contain at least one uppercase letter, one digit, one special character, "
            "and should not have non-printing symbols."
        )
