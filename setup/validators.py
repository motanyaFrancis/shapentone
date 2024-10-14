from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_number_min(value):
    if value < 0:
        raise ValidationError(_('%(value)s must be greater or equal to 1'),
                              params={'value': value},)
