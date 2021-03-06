"""
Custom form validators for this app.

"""
import os.path

from django.core.exceptions import ValidationError


def validate_isdir(value):
    """Validate if ``value`` is an existing directory."""
    if not os.path.isdir(value):
        raise ValidationError(f'{value}: No such directory.')
