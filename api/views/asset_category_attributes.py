"""Module for asset category attribute views"""  # pylint: disable=F0002

from flask_restplus import Resource  # pylint: disable=E0401

from main import api
from api.utilities.validators.validate_id import validate_id
from ..models.asset_category import AssetCategory
from ..utilities.model_serializers.attribute import AttributeSchema
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_json_request import validate_json_request


@api.route('/asset-categories/<string:id>/attributes')
class AssetCategoryAttributes(Resource):
    """Resource class for asset categories attributes"""

    @token_required
    @validate_id
    def get(self, id):  # pylint: disable=C0103, w0622,R0201
        """Get attributes of an asset category"""

        asset_category = AssetCategory.get_or_404(id)

        attributes_schema = AttributeSchema(many=True, exclude=['deleted'])
        attributes = attributes_schema.dump(
            asset_category.attributes.filter_by(deleted=False)).data

        return {
            'status': 'success',
            'message': 'Asset category attributes retrieved',
            'data': {
                'name': asset_category.name,
                'customAttributes': attributes
            }
        }, 200
