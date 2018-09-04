"""Module for center endpoints tests"""

from os import getenv

from flask import json  #pylint:disable=E0401

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.models.asset import Asset
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.models.user import User
from api.models.role import Role
from .mocks.center import VALID_CENTER, INCOMPLETE_DATA, INVALID_CENTER

API_V1_BASE_URL = getenv('API_BASE_URL_V1')


class TestCenterEndpoints:
    """
    Center endpoints tests
    """

    def test_create_center_success(self, client, auth_header, init_db):
        """
        Test successfully creating a center

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(object): fixture to initialize the test database
        """

        center = json.dumps(VALID_CENTER)
        response = client.post(
            f'{API_V1_BASE_URL}/centers', data=center, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['data']['name'] == VALID_CENTER['name']
        assert response_json['data']['image'] == VALID_CENTER['image']

    def test_create_center_failure_with_existing_data(  #pylint:disable=C0103
            self, client, auth_header):
        """
        Test that error is returned when
        creating an already existing center

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
        """

        center = json.dumps(VALID_CENTER)
        response = client.post(
            f'{API_V1_BASE_URL}/centers', data=center, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format('Center')

    def test_create_center_failure_without_token(self, client):  #pylint:disable=C0103
        """
        Test that an error is returned when trying to
        create a center without a valid token

        Parameters:
            client(object): fixture to get flask test client
        """

        center = json.dumps(VALID_CENTER)
        response = client.post(f'{API_V1_BASE_URL}/centers', data=center)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_create_center_failure_with_incomplete_data(  #pylint:disable=C0103
            self, client, auth_header):
        """
        Test that an error is returned when creating
        a center with incomplete data

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
        """

        center = json.dumps(INCOMPLETE_DATA)
        response = client.post(
            f'{API_V1_BASE_URL}/centers', data=center, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['image'][
            0] == 'Missing data for required field.'

    def test_create_center_failure_with_invalid_data(  #pylint:disable=C0103
            self, client, auth_header):
        """
        Test that an error is returned when creating
        a center with invalid data

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
        """

        center = json.dumps(INVALID_CENTER)
        response = client.post(
            f'{API_V1_BASE_URL}/centers', data=center, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['name'][0] == serialization_errors[
            'string_characters']

    def test_hard_delete_center(  #pylint:disable=C0103
            self, client, init_db, test_center, auth_header):  # pylint: disable=W0613
        """
            Tests for hard deleting a center with neither child user nor
            child asset
        """
        test_center.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{test_center.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'hard_delete'].format(test_center.name)

    def test_soft_delete_center_with_user(  #pylint:disable=C0103
            self, client, init_db, test_center, auth_header):  # pylint: disable=W0613
        """
            Tests for soft deleting a center with an associated user
        """
        test_role = Role(title='dev').save()
        User(
            id='-GTHFDR56765',
            name='Duke',
            email='duke@abc.com',
            center_id=test_center.id,
            role_id=test_role.id).save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{test_center.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'soft_delete'].format(test_center.name)

    def test_soft_delete_center_with_asset(  #pylint:disable=C0103,R0913
            self,
            client,
            init_db,
            test_center,
            test_asset_category,  # pylint: disable=W0613
            auth_header):
        """
            Tests for soft deleting a center with an associated asset
        """
        test_center.save()
        Asset(
            id='-6665trfdUYT',
            asset_category_id=test_asset_category.id,
            tag='DukeXYZ',
            center_id=test_center.id).save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{test_center.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'soft_delete'].format(test_center.name)

    def test_delete_center_not_found(self, client, init_db, auth_header):  # pylint: disable=W0613
        """
            Tests that 404 is returned for an attempt to delete a
            non-existent center
        """

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/-L6YY54rfd98GTY', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Center')

    def test_delete_center_invalid_id(  #pylint: disable=C0103
            self, client, init_db, auth_header):  #pylint: disable=W0613
        """
        Tests that 400 is returned when id is invalid
        """
        response = client.delete(
            f'{API_V1_BASE_URL}/centers/-LX%%%tghrfe5', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_delete_center_without_token(  #pylint: disable=C0103
            self, client, init_db):  #pylint: disable=W0613
        """
        Tests that 401 is returned when token is not provided
        """
        response = client.delete(f'{API_V1_BASE_URL}/centers/-LX%%%tghrfe5')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
