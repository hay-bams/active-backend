"""Module that tests the functionalities of dynamic filter"""
from os import getenv

import pytest
from flask import json
from werkzeug.datastructures import ImmutableMultiDict

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import filter_errors
from api.middlewares.base_validator import ValidationError
from api.models.asset_category import AssetCategory

api_v1_base_url = getenv("API_BASE_URL_V1")


class TestQueryFilter:
    """
    Class that holds methods for testing dynamic filter request
    """

    def test_for_wrong_formatted_query(
            self, client, auth_header):
        """
        Check the format of the filter string
        Should return error for a badly-formatted query. A well-formatted
        query takes the form 'xxx,yyy,zzz' where xxx is the column to filter
        (eg, name), yyy is the comparator (eg eq) and zzz is the value
        to compare

        Asserts that the request fails due to badly-formatted filter condition
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name;eq,Laptop',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == filter_errors[
            "INVALID_FILTER_FORMAT"].format("name;eq,Laptop")

    def test_for_request_without_filter_query(
            self, client, init_db, auth_header, multiple_categories):
        """
        Assert that all records are fetched when no filter is provided
        Tests if no filter query is specified. if no filter query
        is specified, the search should returned all the records in the
        specified category
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 3

    def test_for_request_with_one_filter_query(
            self, client, init_db, auth_header, multiple_categories):
        """
        Test a single filter condition
        the request should return only two records that satisfy the condition
        of the query string

        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like,ap',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 2
        assert not any(
            category["name"] == "Chromebook" for category in
            response_json["data"])
        assert any(category["name"] == "Laptop" for category in
                   response_json["data"])
        assert any(category["name"] == "Apple" for category in
                   response_json["data"])

    def test_for_request_with_multiple_filter_query(
            self, client, init_db, auth_header, multiple_categories):
        """
        Test a query string of two filter conditions
        The request should return only one record that satisfy the condition
        of the query string

        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,'\
            'like,ap&where=name,ne,Apple', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 1
        assert not any(
            category["name"] == "Chromebook" for category in
            response_json["data"])
        assert any(category["name"] == "Laptop" for category in
                   response_json["data"])
        assert not any(category["name"] == "Apple" for category in
                       response_json["data"])


class TestDynamicFilterClass:
    """
    Class that holds test methods for testing DynamicFilter class
    """

    def test_invalid_filter_format(self, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument is badly-formatted. A well-formatted
        argument takes the form ImmutableMultiDict([('where', 'xxx,yyy,zzz')])
        where xxx is the column to filter (eg, name), yyy is the comparator
        (eg eq) and zzz is the value to compare
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(
                ImmutableMultiDict([('where', 'name;like')]))

    def test_invalid_column_name(self, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument has a column not found in the specified.
        table. In this case AssetCategory table has no age column
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(
                ImmutableMultiDict([('where', 'age,eq,19')]))

    def test_invalid_filter_operator(self, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument has a wrong operator. Valid operators
        include: eq, ne, like, ge, gl, lt, gt
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(ImmutableMultiDict(
                [('where', 'age,bad_comparator,19')]))

    def test_valid_query(self, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter successfully
        executes and returns the expected result.
        """
        result = dynamic_filter.filter_query(ImmutableMultiDict(
            [('where', 'name,like,ap')])).all()
        names = [record.name for record in result]
        assert len(names) == 2
        assert isinstance(names, list)
        assert 'Apple' in names
        assert 'Laptop' in names
        assert 'Chromebook' not in names
