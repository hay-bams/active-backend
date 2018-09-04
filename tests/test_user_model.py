"""Module to test user model"""

from api.models import User


class TestUserModel:
    """Test user model"""

    def test_new_user(self, init_db, new_user):
        """Test for creating a new user"""
        assert new_user == new_user.save()

    def test_get(self, new_user):
        """Test for get method"""
        assert User.get(new_user.id) == new_user

    def test_update(self, new_user):
        """Test for update method"""
        new_user._update(name='Ayobami')
        assert new_user.name == 'Ayobami'

    def test_count(self, new_user):
        """Test for count of users"""
        assert new_user.count() == 1

    def test_query(self, new_user):
        """Test for query method"""
        user_query = new_user._query()
        assert user_query.count() == 1
        assert isinstance(user_query.all(), list)
        assert user_query.filter_by(name='Ayobami').first() == new_user
        assert user_query.filter(new_user.name == 'Ayobami').count() == 1
        assert isinstance(
            user_query.filter(new_user.name == 'Ayobami').all(), list)

    def test_delete(self, new_user, request_ctx,
                    mock_request_obj_decoded_token):
        """Test for delete method"""
        new_user.delete()
