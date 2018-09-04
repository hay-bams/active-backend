"""Module to test attribute resource endpoint"""

from os import getenv

from flask import json

from api.models.asset_category import AssetCategory
from api.models.attribute import Attribute
from api.utilities.constants import CHARSET

api_base_url_v1 = getenv('API_BASE_URL_V1')


class TestAttribute:
    """Attribute endpoint test"""

    def test_get_asset_category_attributes_with_valid_id(
            self, init_db, client, auth_header):
        """Should return attributes of an asset category"""

        asset_category = AssetCategory(name='HD Screen')
        asset_category.save()
        choices = ['red', 'blue']
        attributes = Attribute(
            label='color',
            _key='color',
            is_required=False,
            input_control='text-area',
            choices=','.join(choices),
            asset_category_id=asset_category.id)
        attributes.save()

        response = client.get(
            f'{api_base_url_v1}/asset-categories/{asset_category.id}/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['name'] == 'HD Screen'
        assert type(response_json['data']['customAttributes']) == list
        assert len(response_json['data']['customAttributes']) == 1
        assert response_json['data']['customAttributes'][0]['label'] == 'color'
        assert response_json['data']['customAttributes'][0][
            'inputControl'] == 'text-area'
        assert response_json['data']['customAttributes'][0][
            'choices'] == choices
        assert response_json['data']['customAttributes'][0][
            'isRequired'] == False

    def test_get_asset_category_attributes_with_invalid_id(
            self, init_db, client, auth_header):
        """Should raise an exception for invalid asset category id"""

        response = client.get(
            f'{api_base_url_v1}/asset-categories/@not-valid@/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Invalid id in parameter'

    def test_get_asset_category_attributes_with_non_exiting_or_deleted_id(
            self, init_db, client, auth_header):
        """Should raise an exception when asset category id is not found"""

        response = client.get(
            f'{api_base_url_v1}/asset-categories/-not-Found/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Asset category not found'
