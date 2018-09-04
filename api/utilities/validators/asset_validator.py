"""Module for validating asset input data"""
from ...models import AssetCategory, Asset
from ...middlewares.base_validator import ValidationError
from ..model_serializers.asset import AssetSchema
from ..messages.error_messages import serialization_errors
from .validate_id import is_valid_id


def validate_attributes(asset_category, request_data, edit):
    """Helper function to validate asset input data"""

    if 'tag' not in request_data or not request_data['tag'].strip():
        raise ValidationError(
            dict(message=serialization_errors['attribute_required'].format(
                'tag')),
            400)

    if not edit:
        if Asset.query.filter(
                Asset.tag == request_data.get('tag', None)).first():
            raise ValidationError(
                dict(message=serialization_errors['duplicate_asset'].format(
                    request_data.get('tag'))),
                409)

    if 'customAttributes' in request_data:
        required_attributes = asset_category.attributes.filter_by(
            deleted=False, is_required=True).all()
        all_attributes = asset_category.attributes.filter_by(
            deleted=False).all()
        required_attribute_keys = [
            attribute._key for attribute in required_attributes  #pylint: disable=W0212
        ]
        attribute_keys = [attribute._key for attribute in all_attributes]  #pylint: disable=W0212

        for request_attribute in request_data['customAttributes']:
            if request_attribute not in attribute_keys:
                raise ValidationError(
                    dict(message=serialization_errors['unrelated_attribute']
                         .format(request_attribute)),
                    400)

            if request_attribute in required_attribute_keys:
                required_attribute_keys.remove(request_attribute)

        if required_attribute_keys:
            for attr in required_attribute_keys:
                raise ValidationError(
                    dict(message=serialization_errors['attribute_required']
                         .format(attr)),
                    400)


def asset_data_validators(request, edit):
    """Data parsing and validation helper for asset POST and PATCH endpoints.

    :param request: The flask request object for the endpoint
    :type request: Flask Request Object

    :param edit: Whether the asset is being edited
    :type edit: bool

    :return: Deserialized and validated asset data from the request body.
    """

    request_data = request.get_json()

    if 'assetCategoryId' not in request_data:
        raise ValidationError({
            "message":
            serialization_errors["key_error"].format("assetCategoryId")
        }, 400)

    if not is_valid_id(request_data['assetCategoryId']):
        raise ValidationError(
            {
                "message": serialization_errors["invalid_category_id"]
            }, 400)

    asset_category = AssetCategory.get_or_404(request_data['assetCategoryId'])

    validate_attributes(asset_category, request_data, edit=edit)

    asset_schema = AssetSchema()

    return asset_schema.load_object_into_schema(request_data)
