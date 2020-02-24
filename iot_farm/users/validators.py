import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import settings as user_settings


@deconstructible
class MobileValidator(validators.RegexValidator):
    regex = user_settings.MOBILE_REGEX
    message = _(
        user_settings.MOBILE_ERROR
    )
    flags = re.IGNORECASE | re.MULTILINE
