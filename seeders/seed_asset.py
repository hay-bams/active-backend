"""Module to seed asset table"""

from api.models import AssetCategory, Asset


def seed_asset():
    # Apple tv assets
    apple_tv_category = AssetCategory._query().filter_by(
        name='Apple TV').first()
    custom_attributes = {
        'color': 'red',
        'warranty': '2019-02-08',
        'size': '13.3inches'
    }
    apple_tv_assets_data = [
        {
            'tag': 'AND/345/EWRD',
            'serial': 'GRGR334TGD',
            'asset_category_id': apple_tv_category.id,
            'custom_attributes': custom_attributes
        },
        {
            'tag': 'AND/654/FWED',
            'serial': 'SDW435OOJD',
            'asset_category_id': apple_tv_category.id,
            'custom_attributes': custom_attributes
        },
        {
            'tag': 'AND/234/FJAD',
            'serial': 'JHDHG23JJD',
            'asset_category_id': apple_tv_category.id,
            'custom_attributes': custom_attributes
        },
        {
            'tag': 'AND/345/AFWD',
            'serial': 'AFWEF34OFD',
            'asset_category_id': apple_tv_category.id,
            'custom_attributes': custom_attributes
        }
    ]

    apple_tv_assets = [
        Asset(
            tag=data['tag'], serial=data.get('serial'),
            asset_category_id=data['asset_category_id'],
            custom_attributes=data['custom_attributes']
        ) for data in apple_tv_assets_data
    ]

    for asset in apple_tv_assets:
        asset.save()

    # Chromebooks assets
    chromebooks_category = AssetCategory._query().filter_by(
        name='ChromeBooks').first()
    chromebooks_assets_data = [
        {
            'tag': 'AND/3235/ERR',
            'serial': 'NBA220FWE',
            'asset_category_id': chromebooks_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/634/FHE',
            'serial': 'NTW456RGR',
            'asset_category_id': chromebooks_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/246/TRA',
            'serial': 'JAA556EGR',
            'asset_category_id': chromebooks_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/875/HJR',
            'serial': 'AWF232EGG',
            'asset_category_id': chromebooks_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        }
    ]

    chromebooks_assets = [
        Asset(
            tag=data['tag'], serial=data.get('serial'),
            custom_attributes=data['custom_attributes'],
            asset_category_id=data['asset_category_id']
        ) for data in chromebooks_assets_data
    ]

    for asset in chromebooks_assets:
        asset.save()

    # Laptops assets
    laptops_category = AssetCategory._query().filter_by(name='Laptops').first()
    laptops_asset_data = [
        {
            'tag': 'AND/K32/001',
            'serial': 'KDJS43JN432LP',
            'asset_category_id': laptops_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/K32/002',
            'serial': 'KDJS43JN432LP',
            'asset_category_id': laptops_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/K32/003',
            'serial': 'KDJS43JN432LP',
            'asset_category_id': laptops_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/K32/004',
            'serial': 'KDJS43JN432LP',
            'asset_category_id': laptops_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        },
        {
            'tag': 'AND/K32/005',
            'serial': 'KDJS43JN432LP',
            'asset_category_id': laptops_category.id,
            'custom_attributes': {'warranty': '2019-02-08'}
        }
    ]

    laptops_asset = [
        Asset(
            tag=data['tag'], serial=data.get('serial'),
            custom_attributes=data['custom_attributes'],
            asset_category_id=data['asset_category_id']
        ) for data in laptops_asset_data
    ]

    for asset in laptops_asset:
        asset.save()
