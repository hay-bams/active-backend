"""Module for asset category resource."""

from flask_restplus import Resource
from flask import request, jsonify

from api.models import AssetCategory
from api.models import Asset
from main import api
from api.middlewares.token_required import token_required
from api.utilities.model_serializers.asset_category import (
    AssetCategorySchema, UpdateAssetCategorySchema,
    EagerLoadAssetCategoryAttributesSchema)
from ..utilities.model_serializers.asset import AssetSchema
from api.utilities.model_serializers.attribute import (AttributeSchema,
                                                       UpdateAttributeSchema)
from api.middlewares.base_validator import ValidationError
from api.utilities.validators.validate_id import validate_id
from api.utilities.messages.error_messages import serialization_errors
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.constants import EXCLUDED_FIELDS


@api.route('/asset-categories')
class AssetCategoryResource(Resource):
    """
    Resource class for peforming crud on the asset categories
    """

    @token_required
    @validate_json_request
    def post(self):
        """
        Creates asset categories and the corresponding attributes
        """

        request_data = request.get_json()

        asset_category_schema = AssetCategorySchema()
        asset_category = asset_category_schema.load_object_into_schema(
            request_data)

        attributes_data = request_data.get('customAttributes')

        if attributes_data:
            attributes_schema = AttributeSchema(
                many=True, exclude=['id', 'deleted'])

            attributes = attributes_schema.load_object_into_schema(
                attributes_data)
            asset_category.attributes = attributes
            attributes = attributes_schema.dump(attributes).data
        else:
            raise ValidationError({
                'message':
                serialization_errors['provide_attributes']
            })

        asset_category = asset_category.save()

        response = jsonify({
            "status": 'success',
            "data": {
                "name": asset_category.name,
                "customAttributes": attributes
            }
        })

        response.status_code = 201
        return response


@api.route('/asset-categories/stats')
class AssetCategoryStats(Resource):
    """
    Resource class for getting asset categories and
    their corresponding asset counts
    """

    @token_required
    def get(self):
        """
        Gets asset categories and the corresponding asset count
        """
        asset_categories = AssetCategory._query(request.args)

        asset_category_schema = AssetCategorySchema(
            many=True, exclude=['deleted'])

        return {
            'status': 'success',
            'data': asset_category_schema.dump(asset_categories).data
        }


@api.route('/asset-categories/<string:id>')
class AssetCategoryListResource(Resource):
    """Asset category list resource"""

    @token_required
    @validate_id
    def get(self, id):
        """
        Get a single asset category
        """

        single_category = AssetCategory.get_or_404(id)

        attributes_schema = AttributeSchema(
            many=True, exclude=['choices', 'id', 'deleted'])

        return {
            'status': 'success',
            'data': {
                'name':
                single_category.name,
                'customAttributes':
                attributes_schema.dump(single_category.attributes).data
            }
        }, 200

    @token_required
    @validate_json_request
    @validate_id
    def patch(self, id):
        """
        Updates asset categories and the corresponding attributes
        """

        request_data = request.get_json()

        asset_category_schema = UpdateAssetCategorySchema()
        asset_category_data = asset_category_schema.load_object_into_schema(
            request_data)

        asset_category_name = asset_category_data.get('name')

        asset_category = AssetCategory.get_or_404(id)

        if asset_category_name:
            asset_category._update(name=asset_category_name)

        attributes_data = request_data.get('customAttributes')
        attributes_schema = UpdateAttributeSchema(
            many=True, exclude=['deleted'])

        if attributes_data:
            attributes_schema_data = attributes_schema.load_object_into_schema(
                attributes_data)  # noqa
            for attribute in attributes_schema_data:
                attribute_result = asset_category.attributes.filter_by(
                    id=attribute.get('id')).first()
                if attribute_result:
                    attribute_result._update(**attribute)

        attributes = attributes_schema.dump(
            asset_category.attributes.all()).data

        response = jsonify({
            "status": 'success',
            "data": {
                "name": asset_category.name,
                "customAttributes": attributes
            }
        })

        response.status_code = 200
        return response

    @token_required
    @validate_id
    def delete(self, id):
        """
        Soft delete asset categories
        """

        single_category = AssetCategory.get_or_404(id)
        single_category.delete()

        return {
            'status': 'success',
            'message': 'category deleted successfully'
        }


@api.route('/asset-categories')
class AssetCategoryList(Resource):
    """
    Resource class for getting the list of asset categories and
    their corresponding asset counts
    """

    @token_required
    def get(self):
        """
        Gets list of asset categories and the corresponding asset count
        """
        asset_categories_schema = AssetCategorySchema(
            many=True, exclude=['deleted'])

        if request.args:
            include = request.args.get('include')
            if include and include.lower() == 'attributes':
                asset_categories = AssetCategory._query()
                eager_loaded_schema = EagerLoadAssetCategoryAttributesSchema(
                    many=True, exclude=['deleted'])
                data = eager_loaded_schema.dump(asset_categories).data
            else:
                asset_categories = AssetCategory._query(request.args)
                data = asset_categories_schema.dump(asset_categories).data
        else:
            asset_categories = AssetCategory._query()
            data = asset_categories_schema.dump(asset_categories).data

        return {'status': 'success', 'data': data}


@api.route('/asset-categories/<string:id>/assets')
class AssetCategoryAsset(Resource):
    """
    Resource class for getting the list of assets that belong to an asset category  # noqa
    """

    @token_required
    @validate_id
    def get(self, id):
        """
        Gets list of assets that belong to an asset category
        """

        asset_category = AssetCategory.get_or_404(id)
        assets = AssetSchema(
            many=True, exclude=EXCLUDED_FIELDS).dump(
                asset_category.assets.filter_by(deleted=False)).data

        return {
            'status':
            'success',
            'message':
            serialization_errors['asset_category_assets'].format(
                asset_category.name),  # noqa
            'data':
            assets
        }
