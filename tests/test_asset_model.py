from api.models import Asset, AssetCategory


class TestAssetModel:
    def test_new_asset(self, new_asset_category, init_db):
        asset = Asset(tag='AND/345/EWR', serial='GRGR334TG')
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        assert asset == asset.save()

    def test_count(self):
        assert Asset.count() == 1

    def test_query(self):
        asset_query = Asset._query()
        assert asset_query.count() == 1
        assert isinstance(asset_query.all(), list)

    def test_update(self, new_asset_category):
        new_asset_category.assets[0]._update(serial='FFE323DF')
        assert new_asset_category.assets[0].serial == 'FFE323DF'

    def test_get(self, new_asset_category):
        asset = Asset(tag='AND/345/EWH', serial='GFGR634TG')
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        asset.save()
        assert Asset.get(asset.id) == asset

    def test_delete(self, new_asset_category, request_ctx,
                    mock_request_obj_decoded_token):
        new_asset_category.assets[0].delete()
