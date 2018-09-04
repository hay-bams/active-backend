"""Module for marshmallow base schema tests."""
import datetime

import pytest
from flask import json

from api.utilities.model_serializers.base_schemas import (BaseSchema,
                                                          AuditableBaseSchema)


class TestBaseSchema(object):
    """Base schema tests."""

    @pytest.fixture(scope='class')
    def base_schema_instance(self):
        """Return base schema instance."""
        return BaseSchema()

    @pytest.fixture(scope='class')
    def base_schema_data(self):
        """Return base schema test data."""
        return {'id': 'abcd', 'deleted': False}

    def test_deserialization_base_schema(
            self,
            base_schema_instance,  #pylint: disable=C0103
            base_schema_data):
        """
        Test base schema deserialization.

        Test base schema ignores read only input data and returns empty dict.
        Test the load objects and load json into schema methods.
        """
        json_data = json.dumps(base_schema_data)

        assert base_schema_instance.load_json_into_schema(json_data) == {}
        assert base_schema_instance.load_object_into_schema(
            base_schema_data) == {}

    def test_serialization_base_schema(self, base_schema_instance,
                                       base_schema_data):
        """
        Test base schema serialization.

        Test base schema correctly serializes python dicts into json.
        """
        schema_output = base_schema_instance.dumps(base_schema_data).data
        assert json.loads(schema_output) == base_schema_data


class TestAuditableSchema(object):
    """Auditable schema tests."""

    @pytest.fixture(scope='class')
    def auditable_base_schema_instance(self):
        """Return base schema instance."""
        return AuditableBaseSchema()

    @pytest.fixture(scope='class')
    def auditable_base_schema_data(self):
        """Return base schema test data."""
        now = datetime.datetime.utcnow()
        user_id = '-LH8bKHHH3assedcMScV'

        return {
            'created_at': now,
            'updated_at': now,
            'deleted_at': now,
            'created_by': user_id,
            'updated_by': user_id,
            'deleted_by': user_id
        }

    def test_deserialization_auditable_schema(
            self,
            auditable_base_schema_data,  #pylint: disable=C0103
            auditable_base_schema_instance):
        """
        Test auditable base schema deserialization.

        Test auditable base schema ignores read only input data and returns
        empty dict. Test the load objects and load json into schema methods.
        """
        json_data = json.dumps(auditable_base_schema_data)

        assert auditable_base_schema_instance.load_json_into_schema(
            json_data) == {}
        assert auditable_base_schema_instance.load_object_into_schema(
            auditable_base_schema_data) == {}

    def test_serialization_auditable_base_schema(
            self,  #pylint: disable=C0103
            auditable_base_schema_instance,  #noqa
            auditable_base_schema_data):
        """
        Test auditable_base schema serialization.

        Test auditable_base schema correctly serializes python dicts into json.
        """
        schema_output = auditable_base_schema_instance.dumps(
            auditable_base_schema_data).data
        # format input datetime strings to iso format
        data = {}
        date_fields = ['created_at', 'updated_at', 'deleted_at']
        id_fields = ['created_by', 'updated_by', 'deleted_by']
        for key in id_fields:
            data[key] = auditable_base_schema_data[key]
        for key in date_fields:
            data[key] = auditable_base_schema_data[key].replace(
                tzinfo=datetime.timezone.utc).isoformat()

        assert json.loads(schema_output) == data

    def test_serialization_invalid_data(self, auditable_base_schema_instance):
        """
        Test auditable base schema serialization.

        Test serialization with invalid data.
        """
        invalid_data = {
            'created_at': 'now',
            'updated_at': 'now',
            'deleted_at': 'now',
            'created_by': 1,
            'updated_by': 3,
            'deleted_by': 4
        }

        assert auditable_base_schema_instance.dumps(
            invalid_data).errors != '{}'
