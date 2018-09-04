"""Module to test endpoint to delete a person"""

from os import getenv

from flask import json

from api.models import Center, User
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import (jwt_errors,
                                                   serialization_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

API_V1_BASE_URL = getenv('API_BASE_URL_V1')


class TestDeletePersonEndpoint:
    """Test delete a person endpoint"""

    def test_delete_a_person_without_authentication(self, init_db, client,
                                                    new_role):  # pylint: disable=C0103, W0613
        """
        Test delete a person endpoint without authentication.

        :param client: request client fixture
        :return: None
        """

        center = Center(name='Lagos', image={'url': 'image url'})
        center.save()
        new_role.save()
        person = User(
            name='Tony',
            email='tony@example.com',
            image_url='url',
            role_id=new_role.id,
            center_id=center.id)
        person.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/{person.id}')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_delete_a_person_for_invalid_center_or_person_id(  # pylint: disable=C0103
            self, init_db, client, auth_header):  # pylint: disable=W0613
        """
        Test delete a person when an invalid center or person id is supplies
        :param init_db: initialize the database
        :param client: request client
        :param auth_header: authentication header
        :return: None
        """

        center = Center(name='Kigali', image={'url': 'image url'})
        center.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/@invalid_id@/people/person_id',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/@invalid_id@',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_delete_a_person_for_non_existing_center_or_person(  # pylint: disable=C0103
            self, init_db, client, auth_header):  # pylint: disable=C0103, W0613
        """
        Test delete a person endpoint for a non existing center or person.

        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        center = Center(name='Nairobi', image={'url': 'image url'})
        center.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/non_existing_center/people/person_id',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Center not found'

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/non_existing_id',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'person_not_found']

    def test_delete_a_person_for_deleted_center_or_person(  # pylint: disable=C0103, R0913
            self,
            init_db,  # pylint: disable=W0613
            client,
            auth_header,
            request_ctx,  # pylint: disable=W0613
            mock_request_obj_decoded_token, new_role):  # pylint: disable=C0103, W0613
        """
        Test delete a person endpoint for a deleted center or person.

        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        center = Center(name='Cairo', image={'url': 'image url'})
        center.save()
        new_role.save()
        person = User(
            name='Mary',
            email='mary@example.com',
            image_url='url',
            role_id=new_role.id,
            center_id=center.id)
        person.save()
        person.delete()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/{person.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'person_not_found']

        center.delete()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/{person.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Center not found'

    def test_delete_a_person_for_a_successful_request(  # pylint: disable=C0103
            self, init_db, client, auth_header, new_role):  # pylint: disable=W0613
        """
        Test delete a person endpoint for when the request is successful
        :param init_db: initialize database fixture
        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        center = Center(name='Kampala', image={'url': 'image url'})
        center.save()
        new_role.save()
        person = User(
            name='Paul',
            email='paul@example.com',
            image_url='url',
            role_id=new_role.id,
            center_id=center.id)
        person.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/centers/{center.id}/people/{person.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'person_deleted'].format(person.name)
