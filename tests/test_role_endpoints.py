"""
Module of tests for asset endpoints
"""
from os import getenv
from flask import json
from api.utilities.constants import CHARSET

BASE_URL = getenv('API_BASE_URL_V1')

class TestRoleEndpoints:
    """
    Tests for getting roles
    """
    def test_get_role_endpoint(self, client, init_db, auth_header, new_roles):
        """
        Test for getting roles
        """
        for role in new_roles:
            role.save()
        response = client.get(f'{BASE_URL}/roles', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
