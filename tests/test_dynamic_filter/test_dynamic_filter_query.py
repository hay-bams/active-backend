from os import getenv

import pytest
from flask import json

from api.middlewares.base_validator import ValidationError
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import filter_errors

api_v1_base_url = getenv('API_BASE_URL_V1')


class TestDynamicFilter:
    """
     Dynamic filter test
    """
    def test_invalid_operator_in_query(self, client, init_db, auth_header):

        """
        The accepted operator for filtering consists of the following
        :param like, eq, lt, ne, gt, le, ge

        any operator other than those should throw an invalid operator error
        and return an error in this format

        :return {
            "message": "invalid operator, valid operators are 'like, eq, lt, 
                        ne, gt, le, ge",
            "status": "error"
        }
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?where=deleted,@@,true',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors['INVALID_OPERATOR']

    def test_invalid_delete_attr_in_query(self, client, init_db, auth_header):
        """
        The delete attribute for filtering should be a boolean value,
        anything other than a boolean should throw an error and return a
        response in this format

        :return {
            "message": "deleted should be of type bool",
            "status": "error"
        }
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?where=deleted,eq,@@l',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_DELETE_ATTRIBUTE']

    def test_invalid_date_attr_in_query(self, client, init_db, auth_header):
        """
        Any date attribute passed for filtering should be a valid date format,
        anything other than that should throw an error and return a
        response in this format

        :return {
            "message": "Invalid datetime format",
            "status": "error"
        }
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?where=created_at,eq,200',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_DATE'].format('200')
