"""Module to test asset as csv data file"""

from os import getenv

from flask import json

from api.models.asset_category import AssetCategory
from api.models.attribute import Attribute
from api.models.asset import Asset
from api.utilities.constants import CHARSET

API_BASE_URL_V1 = getenv('API_BASE_URL_V1')


class TestAssetCsvResource:
    """Assets csv data files tests"""

    def test_export_assets_as_csv_without_authentication(
            self, init_db, client):  # pylint: disable=W0613
        """Should return error for an unauthenticated user"""

        asset_category = AssetCategory(name='TV')
        asset_category.save()

        response = client.get(
            f'{API_BASE_URL_V1}/asset-categories/{asset_category.id}/assets/export'  # noqa
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Bad request. Header does not ' \
                                           'contain an authorization token.'

    def test_export_assets_as_csv_for_non_existing_asset_category(
            self, init_db, client, auth_header):  # pylint: disable=W0613
        """Should return error when asset category is not found"""

        response = client.get(
            f'{API_BASE_URL_V1}/asset-categories/not-existing-id/assets/export',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Asset category not found'

    def test_export_assets_as_csv_success(self, init_db, client, auth_header):  # pylint: disable=W0613
        """
        Should return csv data file with assets properties
        """

        asset_category = AssetCategory(name='iPhone')
        asset_category.save()
        attributes = Attribute(
            label='color',
            _key='color',
            is_required=False,
            input_control='text-area',
            choices='multiple choices',
            asset_category_id=asset_category.id)
        attributes.save()
        assets_data = [{
            'tag': 'AND/1/ERR',
            'serial': 'N2F',
            'asset_category_id': asset_category.id,
            'custom_attributes': {
                'color': 'indigo',
                'warranty': 'expired'
            }
        }, {
            'tag': 'AND/4/FHE',
            'serial': 'N4R',
            'asset_category_id': asset_category.id,
            'custom_attributes': {
                'color': 'indigo',
                'warranty': 'expired'
            }
        }]

        assets = [
            Asset(
                tag=data['tag'],
                serial=data.get('serial'),
                asset_category_id=data['asset_category_id'],
                custom_attributes=data['custom_attributes'])
            for data in assets_data
        ]
        for asset in assets:
            asset.save()

        response = client.get(
            f'{API_BASE_URL_V1}/asset-categories/{asset_category.id}/assets/export',  # noqa
            headers=auth_header)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'color,created_at,serial,tag,warranty\r\n' in response.data
