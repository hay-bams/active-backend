"""Module for asset category database model"""
from marshmallow import fields, post_load

from api.middlewares.base_validator import ValidationError

from .base_schemas import BaseSchema
from .attribute import AttributeSchema
from api.models.asset_category import AssetCategory
from .base_schemas import BaseSchema
from ..validators.name_validator import name_validator
from ..validators.string_length_validators import string_length_60_validator
from ..messages.error_messages import serialization_errors


class AssetCategorySchema(BaseSchema):
    """Asset category model schema"""

    name = fields.String(required=True,
                         validate=(string_length_60_validator,
                                   name_validator),
                         error_messages={
                             'required':
                             serialization_errors['field_required']})
    assets_count = fields.Method(
        'get_asset_counts',
        load_from='assetsCount',
        dump_to='assetsCount',
    )

    @post_load
    def create_asset_category(self, data):
        """Return asset category object after successful loading of data"""
        result = AssetCategory.query.filter_by(name=data['name']).first()
        if not result:
            return AssetCategory(**data)
        raise ValidationError({'message': 'Asset Category already exist'}, 409)

    def get_asset_counts(self, obj):
        return obj.assets_count


class UpdateAssetCategorySchema(BaseSchema):
    """Update Asset category model schema"""

    name = fields.String(validate=(string_length_60_validator, name_validator))


class EagerLoadAssetCategoryAttributesSchema(AssetCategorySchema):
    """Schema for Asset Category with eager loaded attributes"""

    custom_attributes = fields.Method('get_eager_loaded_attributes',
                                      load_from='customAttributes',
                                      dump_to='customAttributes')

    def get_eager_loaded_attributes(self, obj):
        """Get serialized eager loaded attributes"""

        attribute_schema = AttributeSchema(many=True, exclude=['deleted'])
        return attribute_schema.dump(obj.eager_loaded_attributes).data

