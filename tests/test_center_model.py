"""Module for center model tests"""

from api.models import Center


class TestCenterModel:
    def test_new_center(self, new_center, init_db):
        assert new_center == new_center.save()
        assert Center.count() == 1

    def test_update(self, new_center):
        new_center._update(name='Nairobi')
        assert Center.get(new_center.id).name == 'Nairobi'

    def test_get(self, new_center):
        assert Center.get(new_center.id) == new_center

    def test_query(self, new_center):
        center_query = new_center._query()
        assert center_query.count() == 1
        assert isinstance(center_query.all(), list)

    def test_delete(self, new_center, request_ctx,
                    mock_request_obj_decoded_token):
        new_center.delete()
        assert Center.get(new_center.id) is None
