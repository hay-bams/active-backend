"""Module for role schema"""

from marshmallow import fields, post_load

from .base_schemas import AuditableBaseSchema
from ..validators.name_validator import name_validator
from ..messages.error_messages import serialization_errors
from ..validators.string_length_validators import string_length_60_validator


class RoleSchema(AuditableBaseSchema):
    """
    Role model schema
    """
    title = fields.String(
        required=True,
        validate=(string_length_60_validator, name_validator),
        error_messages={'required': serialization_errors['field_required']})

    @post_load
    def convert_title(self, data):
        """Convert role title with the first letter capitalized"""
        data['title'] = data['title'].title()
