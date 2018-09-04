import pytest

from api.models import Asset, Attribute, AssetCategory
from api.middlewares.base_validator import ValidationError


class TestAssetCategoryModel:
    def test_new_asset_category(self, new_asset_category, init_db):
        assert new_asset_category == new_asset_category.save()

    def test_update(self, new_asset_category):
        new_asset_category._update(name='USB Dongles')
        assert new_asset_category.name == 'USB Dongles'

    def test_get(self, new_asset_category):
        assert AssetCategory.get(new_asset_category.id) == new_asset_category

    def test_assets(self, new_asset_category):
        asset = Asset(tag='AND/345/EWR', serial='GRGR334TG')

        new_asset_category.assets.append(asset)
        asset.save()
        new_asset_category.save()
        assert new_asset_category.assets[0] == asset

    def test_attributes(self, new_asset_category):
        attribute = Attribute(
            _key='warranty',
            label='warranty',
            is_required=False,
            input_control='text-area',
            choices='choice'
        )

        new_asset_category.attributes.append(attribute)
        attribute.save()
        new_asset_category.save()
        assert new_asset_category.attributes[0] == attribute

    def test_count(self, new_asset_category):
        assert new_asset_category.count() == 1

    def test_query(self, new_asset_category):
        category_query = new_asset_category._query()
        assert category_query.count() == 1
        assert isinstance(category_query.all(), list)

    def test_delete_asset_category_with_child_relationships(self, new_asset_category):
        with pytest.raises(ValidationError):
            new_asset_category.delete()
