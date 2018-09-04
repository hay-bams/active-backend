import pytest
from api.models import Role
from api.middlewares.base_validator import ValidationError

class TestRoleModel:
    """
    Test
    """
    def test_new_role(self, init_db, new_role):
        role = new_role
        assert role == new_role.save()

    def test_count(self):
        assert Role.count() == 1

    def test_query(self):
        role_query = Role._query()
        assert role_query.count() == 1
        assert isinstance(role_query.all(), list)

    def test_update(self, new_role):
        new_role._update(title='Talent Development Manager')
        assert new_role.title == 'Talent Development Manager'

    def test_delete(self, new_user, new_role, request_ctx,
                    mock_request_obj_decoded_token):
        new_role.delete()
        assert Role.get(new_role.id) is None
