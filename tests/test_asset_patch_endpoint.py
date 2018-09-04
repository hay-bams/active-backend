"""Module for asset patch endpoint."""
from os import getenv

import pytest
from flask import json

from api.models import Asset, AssetCategory, Attribute
from api.models.database import db
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from .mocks.asset import (ASSET_NO_CUSTOM_ATTRS, ASSET_VALID_CUSTOM_ATTRS,
                          ASSET_DATA_EDITS)

BASE_URL = getenv('API_BASE_URL_V1')


@pytest.fixture(scope='module')
def asset_no_attrs(new_asset_category_with_non_deleted_asset):  #pylint: disable=C0103
    """Test asset with no custom attributes."""
    asset = dict(**ASSET_NO_CUSTOM_ATTRS)
    del asset['assetCategoryId']
    del asset['customAttributes']
    asset['asset_category_id'] = new_asset_category_with_non_deleted_asset.id
    asset = Asset(**asset)
    return asset.save()


@pytest.fixture(scope='module')
def asset_with_attrs():  #pylint: disable=C0103
    """Test asset with no custom attributes."""
    category = AssetCategory(name="Test Category")
    category = category.save()

    attributes = [{
        '_key': 'waranty',
        'label': 'waranty',
        'is_required': True,
        'asset_category_id': category.id,
        'input_control': 'Text'
    }, {
        '_key': 'length',
        'label': 'length',
        'input_control': 'Text',
        'asset_category_id': category.id,
        'is_required': False
    }]

    for attribute in attributes:
        db.session.add(Attribute(**attribute))  #pylint: disable=E1101
    db.session.commit()  #pylint: disable=E1101

    ASSET_VALID_CUSTOM_ATTRS['asset_category_id'] = category.id
    asset = Asset(**ASSET_VALID_CUSTOM_ATTRS)
    return asset.save()


class TestAssetPatchEndpoint:
    """Class for Asset resource PATCH endpoint."""

    def test_edit_asset_valid_input_no_custom_attrs(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_no_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with no custom attributes with valid
        standard attributes included in request.
        """
        asset = dict(**ASSET_NO_CUSTOM_ATTRS)
        asset['customAttributes'] = {}
        asset.update(
            assetCategoryId=asset_no_attrs.asset_category_id, tag='abcd')
        response = client.patch(
            f'{BASE_URL}/assets/{asset_no_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['asset_edited']

    def test_edit_asset_valid_input_with_custom_attrs(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with valid custom attributes with valid
        standard attributes included in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes')
        asset['customAttributes'] = {'waranty': '1234HH', 'length': '100cm'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['message'] == SUCCESS_MESSAGES['asset_edited']
        assert response_data['data']['customAttributes'] == asset[
            'customAttributes']

    def test_edit_asset_valid_input_with_missing_optional_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with missing optional attributes with
        valid standard attributes included in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes', None)
        asset['customAttributes'] = {'waranty': '100cm'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['message'] == SUCCESS_MESSAGES['asset_edited']

    def test_edit_asset_valid_input_with_invalid_custom_attrs(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with invalid custom attributes with valid
        standard attributes included in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes', None)
        asset['customAttributes'] = {'length': '100cm'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response.status_code == 400
        assert response_data['message'] == serialization_errors[
            'attribute_required'].format('waranty')

    def test_edit_asset_unrelated_custom_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with unrelated attribute and
        valid standard attributes included in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes', None)
        asset['customAttributes'] = {'waranty': '100cm', 'some_attr': 'abcd'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response_data['message'] == serialization_errors[
            'unrelated_attribute'].format('some_attr')
        assert response.status_code == 400

    def test_edit_asset_nonexistent_asset_category(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under nonexistent category.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId='-LEiS7lgOu3VmeEBg5cUtt', **ASSET_DATA_EDITS)
        asset.pop('custom_attributes', None)
        asset['customAttributes'] = {'waranty': '100cm', 'length': 'abcd'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Asset category not found'
        assert response.status_code == 404

    def test_edit_asset_invalid_asset_category_id(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset with invalid category id.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(assetCategoryId='invalid_id@@@', **ASSET_DATA_EDITS)
        asset.pop('custom_attributes', None)
        asset['customAttributes'] = {'waranty': '100cm', 'length': 'abcd'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response_data['message'] == serialization_errors[
            'invalid_category_id']
        assert response.status_code == 400

    def test_edit_asset_missing_tag_with_custom_attrs(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with valid custom attributes with
        missing tag in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes')
        asset.pop('tag')
        asset['customAttributes'] = {'waranty': '1234HH', 'length': '100cm'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response.status_code == 400
        assert response_data['message'] == serialization_errors[
            'attribute_required'].format('tag')

    def test_edit_asset_missing_serial_with_custom_attrs(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):  #pylint: disable=W0621
        """
        Test PATCH asset under category with valid custom attributes with
        missing serial in request.
        """
        asset = dict(**ASSET_VALID_CUSTOM_ATTRS)
        asset.update(
            assetCategoryId=asset_with_attrs.asset_category_id,
            **ASSET_DATA_EDITS)
        asset.pop('custom_attributes')
        asset.pop('serial')
        asset['customAttributes'] = {'waranty': '1234HH', 'length': '100cm'}
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(asset))
        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['message'] == SUCCESS_MESSAGES['asset_edited']
