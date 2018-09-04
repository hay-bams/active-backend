"""Module for assets csv data resource"""

from datetime import date
import dateutil.parser

import flask_excel as excel
from flask_restplus import Resource
from flatten_dict import flatten

from main import api
from ..models.asset_category import AssetCategory
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_id import validate_id
from ..utilities.model_serializers.asset import AssetSchema


@api.route('/asset-categories/<string:id>/assets/export')
class ExportAssets(Resource):
    """Resource class for assets csv data files"""

    @token_required
    @validate_id
    def get(self, id):
        """Download assets under an asset category"""

        asset_category = AssetCategory.get_or_404(id)
        assets = asset_category.assets.filter_by(deleted=False).all()
        asset_schema = AssetSchema(
            many=True,
            exclude=[
                'id', 'asset_category_id', 'deleted', 'deleted_at',
                'created_by', 'deleted_by', 'updated_at', 'updated_by'
            ])
        assets_data = asset_schema.dump(assets).data
        assets_data_record = []

        for asset in assets_data:
            # Flatten the asset dict object so as to have
            # the custom attributes as a separate column in the csv file
            asset_data = flatten(asset, reducer=lambda key1, key2: key2)
            asset_data['created_at'] = dateutil.parser.parse(
                asset_data['created_at']).date()
            assets_data_record.append(asset_data)

        return excel.make_response_from_records(
            assets_data_record,
            'csv',
            file_name=f'{asset_category.name} Assets Export - {date.today()}')
