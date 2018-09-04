""" Module for generic string length validators. """
from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors


def string_length_60_validator(data):
    """
    Checks if given string is at most 60 characters.
    Raises validation error otherwise.
    """
    if len(data) > 60:
        raise ValidationError(
            serialization_errors['string_length'].format('60'))
