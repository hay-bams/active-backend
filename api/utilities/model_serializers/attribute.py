""" Module for Attribute model serialization schema. """

from marshmallow import (fields, post_load, post_dump, validate,
                         validates_schema)
from marshmallow.utils import missing
from humps.camel import case

from .base_schemas import BaseSchema
from ..validators.name_validator import name_validator
from ..validators.string_length_validators import string_length_60_validator
from ..messages.error_messages import serialization_errors
from api.models.attribute import Attribute
from ..validators.input_control_validator import input_control_validation
from ..validators.attributes_validator import (
    validate_attribute_exists, validate_choices, validate_choices_after_dump)


class AttributeSchema(BaseSchema):
    """Attribute model schema"""

    _key = fields.String(load_from='label', dump_to='key')

    label = fields.String(
        required=True,
        validate=(string_length_60_validator, name_validator),
        error_messages={'required': serialization_errors['field_required']})
    is_required = fields.Boolean(
        required=True,
        load_from='isRequired',
        dump_to='isRequired',
        error_messages={'required': serialization_errors['field_required']})
    input_control = fields.String(
        required=True,
        load_from='inputControl',
        dump_to='inputControl',
        validate=(string_length_60_validator, name_validator,
                  input_control_validation),
        error_messages={
            'required': serialization_errors['field_required']  # noqa
        })
    choices = fields.List(fields.String(validate=(string_length_60_validator)))

    @validates_schema
    def validate_choice_decorator(self, data):
        return validate_choices(data)

    @post_load
    def create_attribute(self, data):
        """Return attribute object after successful loading into schema"""

        data['_key'] = case(data['_key'])

        return Attribute(**data)

    @post_dump
    def dump_attribute(self, data):
        """
        Return attribute object after successful dumping as array of strings
        """
        return validate_choices_after_dump(data)


class UpdateAttributeSchema(BaseSchema):
    """Update Attribute model schema"""

    id = fields.String(missing='None', validate=(validate_attribute_exists))

    label = fields.String(
        validate=(string_length_60_validator, name_validator))

    is_required = fields.Boolean(load_from='isRequired', dump_to='isRequired')

    input_control = fields.String(
        load_from='inputControl',
        dump_to='inputControl',
        validate=(string_length_60_validator, name_validator,
                  input_control_validation))

    choices = fields.List(fields.String(validate=(string_length_60_validator)))

    @validates_schema
    def validate_choice_decorator(self, data):
        return validate_choices(data)

    @post_dump
    def dump_attribute(self, data):
        """
        Return attribute object after successful dumping as array of strings
        """

        return validate_choices_after_dump(data)
