"""Module that validates that an invalid input-control is not used """
from marshmallow import ValidationError  #pylint: disable=E0401

from api.utilities.enums import InputControlChoiceEnum
from ..messages.error_messages import serialization_errors


def input_control_validation(value):
    """Check that the supplied input_control is one of the accepted types"""
    input_controls = InputControlChoiceEnum.get_all_choices()
    if value.lower() not in input_controls:
        raise ValidationError(serialization_errors['input_control'].format(
            input_controls=str(input_controls).strip('[]')))
