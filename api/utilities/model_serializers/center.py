"""Module for center schema"""

from marshmallow import fields, post_load

from .base_schemas import AuditableBaseSchema
from ..validators.name_validator import name_validator
from ..messages.error_messages import serialization_errors
from ..validators.string_length_validators import string_length_60_validator


class CenterSchema(AuditableBaseSchema):
    """
    Center model schema
    """
    name = fields.String(
        required=True,
        validate=(string_length_60_validator, name_validator),
        error_messages={'required': serialization_errors['field_required']})
    image = fields.Dict(required=True)

    @post_load
    def convert_name(self, data):
        """Convert center name with the first letter capitalized"""
        data['name'] = data['name'].title()
