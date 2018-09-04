""" Module for asset model schema. """

from marshmallow import fields

from .base_schemas import AuditableBaseSchema
from ..validators.string_length_validators import string_length_60_validator
from ..messages.error_messages import serialization_errors


class AssetSchema(AuditableBaseSchema):
    """Asset model schema"""

    tag = fields.String(
        required=True,
        validate=string_length_60_validator,
        error_messages={'required': serialization_errors['field_required']})

    serial = fields.String(
        validate=string_length_60_validator,
        error_messages={'required': serialization_errors['field_required']})

    custom_attributes = fields.Dict(
        load_from="customAttributes", dump_to="customAttributes")

    asset_category_id = fields.String(
        load_from="assetCategoryId",
        dump_to="assetCategoryId",
        required=True,
        validate=string_length_60_validator,
        error_messages={'required': serialization_errors['field_required']})
