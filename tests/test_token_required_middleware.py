from os import getenv

from flask import json

from api.utilities.messages.error_messages import jwt_errors
from api.utilities.constants import CHARSET
from .helpers.generate_token import generate_token

api_v1_base_url = getenv('API_BASE_URL_V1')


class TestTokenRequiredMiddleware:
    def test_token_required_without_token(self, client):
        response = client.get(f'{api_v1_base_url}/asset-categories/stats')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_token_required_when_a_token_does_not_contain_bearer(self, client):
        response = client.get(f'{api_v1_base_url}/asset-categories/stats',
                              headers={'Authorization': 'bb'})
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['NO_BEARER_MSG']

    def test_token_required_with_invalid_token(self, client):
        response = client.get(f'{api_v1_base_url}/asset-categories/stats',
                              headers={'Authorization': 'Bearer invalid_token'})
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']
        
    def test_token_required_with_expired_token(self, client):
        response = client.get(f'{api_v1_base_url}/asset-categories/stats',
                              headers={'Authorization': generate_token(0)})
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['EXPIRED_TOKEN_MSG']
