from .seed_asset_category import seed_asset_category
from .seed_asset import seed_asset
from .seed_roles import seed_roles


def seed_db():
    seed_asset_category()
    seed_asset()
    seed_roles()
