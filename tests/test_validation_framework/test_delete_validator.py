"""Model delete validator."""
import pytest

from api.models import AssetCategory, Asset, Attribute, User
from api.middlewares.base_validator import ValidationError


class TestDeleteValidator(object):
    """Class to test model delete validator."""

    def test_delete_model_with_no_child_relationships(
            self, init_db, new_user, request_ctx,
            mock_request_obj_decoded_token):
        """Test delete on model with no children."""
        new_user.save()
        assert new_user.delete() is None

    def test_delete_model_with_child_relationships(
            self, init_db, new_asset_category, request_ctx,
            mock_request_obj_decoded_token):
        """Test delete on model with children all deleted."""
        saved_category = new_asset_category.save()
        assert saved_category.delete() is None

    def test_delete_model_with_non_deleted_children(
            self, init_db, new_asset_category_with_non_deleted_asset):  #noqa
        """Test delete on model with a non deleted child instance."""
        with pytest.raises(ValidationError):
            new_asset_category_with_non_deleted_asset.delete()

    def test_delete_model_with_deleted_children(
            self, init_db, new_asset_category_with_deleted_asset):  #noqa
        """Test delete on model with a deleted child instance."""
        assert new_asset_category_with_deleted_asset.delete() is None
