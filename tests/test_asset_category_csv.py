"""Module to test asset category as csv data file"""

from os import getenv

from flask import json

from api.models.asset_category import AssetCategory
from api.models.attribute import Attribute
from api.utilities.constants import CHARSET

api_base_url_v1 = getenv('API_BASE_URL_V1')


class TestAssetCategoryCsvResource:
    """Asset categories csv data files tests"""

    def test_export_asset_categories_as_csv_without_authentication(
            self, init_db, client, auth_header):
        """Should return error for an unauthenticated user"""

        response = client.get(
            f'{api_base_url_v1}/asset-categories/export')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Bad request. Header does not ' \
                                           'contain an authorization token.'

    def test_export_asset_category_as_csv_success(
            self, init_db, client, auth_header):
        """
        Should return csv data file with asset categories names and the assets
        count in each category
        """

        asset_category = AssetCategory(name='HD Screen')
        asset_category.save()
        attributes = Attribute(label='color', _key='color', is_required=False,
                               input_control='text-area',
                               choices='multiple choices',
                               asset_category_id=asset_category.id)
        attributes.save()

        response = client.get(
            f'{api_base_url_v1}/asset-categories/export', headers=auth_header)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'name,assets_count\r\nHD Screen,0\r\n' in response.data
