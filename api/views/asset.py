"""Module that handles asset-related operations"""
from datetime import datetime

from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.datastructures import ImmutableMultiDict

from api.middlewares.token_required import token_required
from api.utilities.model_serializers.asset import AssetSchema
from api.utilities.validators.validate_id import is_valid_id
from api.utilities.validators.asset_validator import (validate_attributes)

from api.models.asset_category import AssetCategory
from ..models.asset import Asset
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.validators.validate_id import validate_id
from api.utilities.validators.asset_validator import asset_data_validators
from main import api
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.helpers.asset_endpoints import create_asset_response
from api.utilities.paginator import pagination_helper
from api.utilities.messages.error_messages import filter_errors
from api.utilities.constants import EXCLUDED_FIELDS


@api.route('/assets')
class AssetResource(Resource):
    """
    Resource class for carrying out CRUD operations on asset entity
    """

    @token_required
    @validate_json_request
    def post(self):  #pylint: disable=R0201
        """
        An endpoint that creates a new asset in the database
        """
        # asset_data_validators function parses and validates request data
        new_asset = Asset(
            created_by=request.decoded_token['UserInfo']['id'],
            created_at=datetime.utcnow(),
            **asset_data_validators(request, edit=False))
        new_asset.save()

        response = create_asset_response(
            new_asset, message=SUCCESS_MESSAGES['asset_created'])

        return response, 201

    @token_required
    def get(self):
        """
        Gets Lists of all assets
        """

        data, pagination_object = pagination_helper(Asset, AssetSchema)

        return jsonify({
            "status": 'success',
            "message": 'Assets fetched successfully',
            "data": data,
            "meta": pagination_object
        })


@api.route('/assets/search')
class SearchAssetResource(Resource):
    @token_required
    def get(self):
        """
        Search Asset by date and warranty
        """
        qry_keys = ('start', 'end', 'warranty_start', 'warranty_end')
        qry_dict = dict(request.args)

        for key in qry_dict:
            if key not in qry_keys:
                raise ValidationError(
                    dict(message=filter_errors['INVALID_COLUMN'].format(key)))

        start = request.args.get('start')
        end = request.args.get('end')
        warranty_start = request.args.get('warranty_start')
        warranty_end = request.args.get('warranty_end')

        qry_list = []
        if start:
            qry_list.append(('where', f'created_at,ge,{start}'))
        if end:
            qry_list.append(('where', f'created_at,le,{end}'))
        if warranty_start:
            qry_list.append(('where', f'warranty,ge,{warranty_start}'))
        if warranty_end:
            qry_list.append(('where', f'warranty,le,{warranty_end}'))

        args = ImmutableMultiDict(qry_list)
        assets = Asset._query(args)

        asset_schema = AssetSchema(many=True, exclude=EXCLUDED_FIELDS)

        return {
            'status': 'success',
            'data': asset_schema.dump(assets).data
        }, 200


@api.route('/assets/<string:id>')
class SingleAssetResource(Resource):
    """Resource class for single asset endpoints."""

    @token_required
    @validate_id
    @validate_json_request
    def patch(self, id):  #pylint: disable=C0103,W0622
        """Endpoint for editing an asset."""

        asset = Asset.get_or_404(id)

        # asset_data_validators function parses and validates request data
        asset._update(  #pylint: disable=W0212
            updated_by=request.decoded_token['UserInfo']['id'],
            updated_at=datetime.utcnow(),
            **asset_data_validators(request, edit=True))

        response = create_asset_response(
            asset, message=SUCCESS_MESSAGES['asset_edited'])

        return response, 200
