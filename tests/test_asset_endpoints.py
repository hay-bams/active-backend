"""module of tests for asset endpoints
"""
from os import getenv

from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages import filter_errors
from api.models import Asset
from .mocks.asset import (ASSET_NO_CUSTOM_ATTRS, ASSET_NO_TAG, ASSET_NO_SERIAL,
                          ASSET_NONEXISTENT_CATEGORY,
                          ASSET_INVALID_CATEGORY_ID, ASSET_EMPTY_CUSTOM_ATTRS,
                          ASSET_TWO, ASSET_THREE, ASSET_FOUR, ASSET_FIVE)

api_v1_base_url = getenv('API_BASE_URL_V1')


class TestAssetEndpoints:
    def test_create_asset_with_invalid_category(self, client, init_db,
                                                auth_header):
        """
        Tests create asset if the supplied asset_category_id exists
        in the database
         """

        data = json.dumps(ASSET_NONEXISTENT_CATEGORY)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_create_asset_with_ASSET_INVALID_CATEGORY_ID(
            self, client, init_db, auth_header):
        """
        Tests if a supplied asset_category_id is in the right format. If it is
        not in the right format, there is no need to make database call
        """

        data = json.dumps(ASSET_INVALID_CATEGORY_ID)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "This asset category id is invalid"

    def test_create_asset_with_missing_tag(self, client, init_db, auth_header,
                                           test_asset_category):
        """
        Tests if a standard attribute is missing in the supplied asset object.
        The asset cartegory does not have custom_attributes
        """

        ASSET_NO_TAG["assetCategoryId"] = test_asset_category.id
        data = json.dumps(ASSET_NO_TAG)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute tag is required"

    def test_create_asset_with_valid_data(self, client, init_db, auth_header,
                                          test_asset_category):
        """
        Test create asset with valid serial and tag for a
        cartegory with no custom attributes
        """

        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"

    def test_create_asset_without_custom_attr(
            self, client, init_db, auth_header, test_asset_category):
        """
        Test create asset when all standard attributes are supplied and no
        custom attribute is supplied
        """

        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute waranty is required"

    def test_create_asset_without_required_custom_attr(
            self, client, init_db, auth_header, test_asset_category):
        """
        Test create asset when the standard atributes and optional custom
        attributes are supplied but required custome attributes are not
        supplied
        """

        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["customAttributes"] = {"length": "15"}
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute waranty is required"

    def test_create_asset_with_all_custom_attr(
            self, client, init_db, auth_header, test_asset_category):
        """
        Test create asset when all standard and custom attributes are
        supplied
        """

        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_without_optional_custom_attr(
            self, client, init_db, auth_header, test_asset_category):
        """
        Test create asset when standard attributes and required
        custom attribute is supplied. The asset is still created even
        though an optional custom attribute is missing
        """

        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        ASSET_TWO["customAttributes"] = {"waranty": "expired"}
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_with_unrelated_custom_attr(
            self, client, init_db, auth_header, test_asset_category):
        """
        Test asset creation with an attribute that is neither a standard
        attribute nor custom attribute of the asset category
        """

        ASSET_FOUR["assetCategoryId"] = test_asset_category.id
        ASSET_FOUR["customAttributes"] = {
            "color": "indigo",
            "waranty": "expired"
        }
        data = json.dumps(ASSET_FOUR)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute color is not"\
            " related to this asset category"

    def test_create_asset_with_invalid_request_type(
            self, client, init_db, auth_header_text, test_asset_category):
        """
        Test create asset when all standard and custom attributes are
        supplied
        """

        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header_text, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Content-Type should be " \
                                           "application/json"

    def test_create_asset_with_duplicate_tag(self, client, init_db,
                                             auth_header, new_asset_category):
        """
        Test creation of assets with duplicate tag.
        """
        new_asset_category.save()
        ASSET_FIVE["asset_category_id"] = new_asset_category.id
        asset_object = Asset(**ASSET_FIVE)
        asset_object.save()
        del ASSET_FIVE["asset_category_id"]
        ASSET_FIVE["assetCategoryId"] = new_asset_category.id
        data = json.dumps(ASSET_FIVE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset with the tag Kinngg Macbook"\
            " already exists"

    def test_get_assets_endpoint(self, client, init_db, auth_header):
        response = client.get(f'{api_v1_base_url}/assets', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['currentPage'] != ''
        assert response_json['meta']['firstPage'] != ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) <= 10

    def test_get_assets_endpoint_pagination(self, client, init_db,
                                            auth_header):
        """
        Should return paginated assets
        """
        response = client.get(
            f'{api_v1_base_url}/assets?page=1&limit=3', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json

        assert response_json['meta']['currentPage'] != ''
        assert response_json['meta']['firstPage'] != ''
        assert response_json['meta']['nextPage'] != ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) <= 3

    def test_get_assets_endpoint_pagination_with_invalid_limit_query_string(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated assets
        with wrong query strings
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1@&limit=>>', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('limit', '>>')

    def test_get_assets_endpoint_pagination_with_invalid_page_query_string(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated assets
        with wrong query strings
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1@&limit=1', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('page', '1@')

    def test_get_assets_endpoint_pagination_with_exceeded_page(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the last page if the page provided exceed
        the total page counts
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1000&limit=1', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        page = response_json['meta']['page']
        assert response_json['meta']['currentPage'].endswith(
            f'page={page}&limit=1')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=1')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'].endswith(
            f'page={page-1}&limit=1')
        assert 'totalCount' in response_json['meta']
        assert 'message' in response_json['meta']
        assert response_json['meta']['message'] == serialization_errors[
            'last_page_returned']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_get_assets_endpoint_pagination_with_exceeded_limit(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the all record if the limit provided exceed
        the total record counts
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1&limit=100', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json

        assert response_json['meta']['currentPage'].endswith(
            'page=1&limit=100')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=100')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_get_assets_endpoint_pagination_with_exceeded_page_and_limit(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the last page and all records if the page provided exceed
        the total page counts and if limit exceed total record count
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1000&limit=100',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        page = response_json['meta']['page']
        assert response_json['meta']['currentPage'].endswith(
            f'page={page}&limit=100')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=100')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'] == ''
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_search_asset_endpoint(self, client, init_db, auth_header,
                                   new_asset_category):
        """
         Test that a list of asset is returned when a search query is provided
        """
        assets_data = [
            dict(
                tag='AND/345/EWH',
                serial='GFGR634TG',
                custom_attributes={'warranty': '2017-11-09'}),
            dict(
                tag='AND/245/EkL',
                serial='GFGR633TG',
                custom_attributes={'warranty': '2018-11-09'})
        ]
        assets = []

        for asset in assets_data:
            new_asset = Asset(**asset)
            new_asset_category.assets.append(new_asset)
            assets.append(new_asset)
        new_asset_category.save()

        url = f'''{api_v1_base_url}/assets/search?start=\
{(assets[0].created_at).date()}&end={(assets[1].created_at).date()}&\
warranty_start={assets[0].custom_attributes['warranty']}&\
warranty_end={assets[0].custom_attributes['warranty']}'''

        response = client.get(url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) > 0
        assert type(response_json['data']) == list

    def test_search_asset_with_invalid_column_name(self, client, auth_header):
        """
        Assert that the correct error message is returned when an invalid
        column is provided.
        """
        response = client.get(
            f'{api_v1_base_url}/assets/search?stat=2018-11-09',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_COLUMN'].format('stat')
