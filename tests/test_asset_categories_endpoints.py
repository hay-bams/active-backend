"Module for asset category endpoint test"

from os import getenv

from flask import json  #pylint: disable=E0401

from api.models.asset_category import AssetCategory
from api.models.asset import Asset
from api.models.attribute import Attribute
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from .mocks.asset_category import (
    valid_asset_category_data, invalid_asset_category_data,
    valid_asset_category_data_without_attributes,
    asset_category_data_without_choices,
    asset_category_with_two_wrong_input_control,
    asset_category_with_one_wrong_input_control)

api_v1_base_url = getenv('API_BASE_URL_V1')  #pylint: disable=C0103


class TestAssetCategoriesEndpoints:  #pylint: disable=R0904
    """"
    Asset Category endpoints test
    """

    def test_asset_categories_stats_endpoint(  #pylint: disable=C0103,R0913,R0201
            self,
            client,
            new_asset_category,
            init_db,  #pylint: disable=W0613
            auth_header,
            request_ctx,  #pylint: disable=W0613
            mock_request_obj_decoded_token):  #pylint: disable=W0613
        """
        Should pass when getting asset categories stats
        """

        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        assert response_json["data"][0]["name"] == "Laptop"
        new_asset_category.delete()

    def test_create_asset_categories_endpoint_with_valid_data(  #pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  #pylint: disable=W0613
        """
        Should pass when valid data is provided
        """

        data = json.dumps(valid_asset_category_data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["data"]["name"] == valid_asset_category_data[
            "name"]
        assert response_json["data"][
            "customAttributes"] == valid_asset_category_data[
                "customAttributes"]
        assert response_json["status"] == "success"

    def test_create_asset_categories_endpoint_with_valid_data_without_attributes(  #pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # #pylint: disable=W0613
        """
        Should fail when valid data without attributes is provided
        """
        data = valid_asset_category_data_without_attributes
        data["name"] = "Seun"
        data = json.dumps(data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            "message"] == "Please provide at least one attribute"
        assert response_json["status"] == "error"

    def test_create_asset_categories_endpoint_without_asset_category_name(  #pylint: disable=R0201,C0103
            self, client, new_asset_category, init_db, auth_header):  #pylint: disable=W0613
        """
        Should fail when asset category name is not data is provided
        """

        data = json.dumps({})
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["name"][0] == serialization_errors[
            "field_required"]

    def test_create_asset_categories_endpoint_with_invalid_attributes_data(  # pylint: disable=R0201, C0103
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should fail when invalid attributes data is provided
        """

        data = invalid_asset_category_data
        data["name"] = "cat"
        data = json.dumps(data)

        data = json.dumps(invalid_asset_category_data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["0"]["label"][
            0] == serialization_errors["field_required"]

    def test_update_asset_category(self, client, init_db, auth_header):  #pylint: disable=R0201,W0613
        """
            Test to Update an asset category without attribute
        """
        asset_category = AssetCategory(name="TestLaptop")
        asset_category.save()
        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"]["customAttributes"], list)

    def test_update_asset_category_with_two_wrong_input_controls(  #pylint: disable=R0201,C0103
            self, client, init_db, auth_header):  #pylint: disable=W0613
        """
        Test to Update an asset category without choices with two wrong input
        controls
        """
        asset_category = AssetCategory(name="TestLaptop b")
        asset_category.save()
        data = json.dumps(asset_category_with_two_wrong_input_control)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["0"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls="'dropdown', 'checkbox', 'radio button', 'textarea', 'text'")
        assert response_json["errors"]["1"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls="'dropdown', 'checkbox', 'radio button', 'textarea', 'text'")

    def test_update_asset_category_with_one_wrong_input_controls(  #pylint: disable=R0201,C0103
            self, client, init_db, auth_header):  #pylint: disable=W0613
        """
        Test to Update an asset category without choices with one wrong input
        controls
        """
        asset_category = AssetCategory(name="TestLaptop b2")
        asset_category.save()
        data = json.dumps(asset_category_with_one_wrong_input_control)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["1"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls="'dropdown', 'checkbox', 'radio button', 'textarea', 'text'")

    def test_update_asset_category_without_choices(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613,C0103
            auth_header):
        """
        Test to Update an asset category without choices when multichoice
        input controls are selected
        """
        asset_category = AssetCategory(name="TestLaptop A")
        asset_category.save()
        data = json.dumps(asset_category_data_without_choices)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["1"]["choices"][
            0] == serialization_errors['choices_required']  # pylint: disable=line-too-long

    def test_update_asset_category_with_fake_id(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with fake id
        """

        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/-llllllll',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_update_asset_category_with_invalid_id(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with invalid id
        """

        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/-llll@@@llll',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_update_asset_category_with_attribute(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with an attribute
        """
        asset_category = AssetCategory(name="TestLaptop")
        attribute_data = valid_asset_category_data["customAttributes"][0]
        attribute_data["_key"] = attribute_data["key"]
        attribute_data["is_required"] = attribute_data["isRequired"]
        attribute_data["input_control"] = attribute_data["inputControl"]
        attribute_data.__delitem__("key")
        attribute_data.__delitem__("isRequired")
        attribute_data.__delitem__("inputControl")
        attribute = Attribute(**attribute_data)
        asset_category.attributes.append(attribute)
        asset_category.save()

        attribute_data["id"] = attribute.id
        data = json.dumps({"attributes": [attribute_data]})

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]["customAttributes"]) > 0

    def test_get_one_asset_category(self, client, init_db, auth_header):  #pylint: disable=R0201,W0613
        """
        Tests that a single asset category can be retrieved
        """
        asset_category = AssetCategory(name="TestLaptop1")
        asset_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["data"]["name"] == "TestLaptop1"
        assert type(response_json["data"]["customAttributes"]) == list

    def test_get_one_asset_category_not_found(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Tests that 404 is returned for an asset category that does not exist
        """
        asset_category = AssetCategory(name="TestLaptop2")
        asset_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/-L2', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_get_one_asset_category_invalid_id(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Tests that 400 is returned for an invalid id
        """
        asset_category = AssetCategory(name="TestLaptop3")
        asset_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/L@@', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_delete_asset_category(self, client, init_db, auth_header):  #pylint: disable=R0201,W0613,C0103
        """
            Tests that a single asset category can be deleted
        """
        asset_category = AssetCategory(name="TestLaptop4")
        asset_category.save()

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"

    def test_delete_asset_category_not_found(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Tests that 404 is returned for a category that does not exist on delete
        """

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/-L2', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_delete_asset_category_invalid_id(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Tests that 400 is returned when id is invalid
        """
        asset_category = AssetCategory(name="TestLaptop5")
        asset_category.save()

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/LX@', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_get_assets_for_non_exisiting_category(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Should return an 404 reponse when a wrong id is provided
        """

        asset_category_id = "wrongid"

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_get_asset_category_with_no_assets(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Should return an empty list if no assets belong to an asset category
        """
        asset_category = AssetCategory(name="Apple Tv 1")
        asset_category.save()

        asset_category_id = asset_category.id

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 0
        assert response_json["message"] == serialization_errors[
            "asset_category_assets"].format(asset_category.name)

    def test_get_asset_category_assets(self, client, init_db, auth_header):  #pylint: disable=R0201,W0613,C0103
        """
        Should return lists of assets that belongs to an asset category
        """
        asset_category = AssetCategory(name="Apple Tv 2")

        asset = Asset(tag="abc", serial="def")
        asset_category.assets.append(asset)
        asset_category.save()
        asset_category_id = asset_category.id

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) != 0
        assert response_json["message"] == serialization_errors[
            "asset_category_assets"].format(asset_category.name)

    def test_asset_categories_list_endpoint(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """a method that tests asset_category list endpoint"""
        response = client.get(
            f'{api_v1_base_url}/asset-categories', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        assert response_json["data"][0]["name"] == "Headset"

    def test_asset_categories_list_endpoint_args(self, client, auth_header):  #pylint: disable=R0201,W0613,C0103,C0111
        asset_category = AssetCategory(name="Laptop6")
        asset_category2 = AssetCategory(name="Chairs")
        asset_category.save()
        asset_category2.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like,chairs',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is 1
        assert response_json["data"][0]["name"] == "Chairs"

        invalid_response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like.chairs',
            headers=auth_header)
        invalid_response_json = json.loads(
            invalid_response.data.decode(CHARSET))

        assert invalid_response.status_code == 400
        assert invalid_response_json["status"] == "error"
        asset_category.delete()
        asset_category2.delete()

    def test_eager_load_attributes(  #pylint: disable=R0201,C0103,C0111
            self,
            client,
            init_db,
            test_asset_category,  #pylint: disable=W0613
            auth_header):
        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"][0]["customAttributes"], list)
        assert len(response_json["data"][0]["customAttributes"]) is not 0

    def test_eager_load_attributes_with_invalid_param(  #pylint: disable=R0201,W0613,C0103,C0111
            self, client, auth_header, test_asset_category):  #pylint: disable=W0613
        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "customAttributes" in response_json["data"][0]
