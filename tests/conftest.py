"""Module for setting up fixtures for testing"""
import os

import pytest
from flask import current_app, request

from main import create_app
from config import config
from api.models.database import db as _db
from api.models import User, Asset, AssetCategory, Attribute, Center, Role
from api.utilities.dynamic_filter import DynamicFilter
from api.utilities.constants import MIMETYPE, MIMETYPE_TEXT
from .helpers.generate_token import generate_token
from api.models.database import db
from tests.mocks.center import VALID_CENTER_FOR_DELETE

config_name = 'testing'
os.environ['FLASK_ENV'] = config_name


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """

    _app = create_app(config[config_name])

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()



@pytest.fixture(scope='module')
def new_roles(app):
    roles = [
        Role(title='Operations Intern'),
        Role(title='Operations Coordinator'),
        Role(title='Operations Assistant'),
        Role(title='Operations Manager'),
    ]
    return roles

@pytest.fixture(scope='module')
def new_role(app):
    role = Role(title='Operations Intern')
    return role

@pytest.fixture(scope='module')
def new_roles(app):
    roles = [
        Role(title='Operations Intern'),
        Role(title='Operations Coordinator'),
        Role(title='Operations Assistant'),
        Role(title='Operations Manager'),
    ]
    return roles


@pytest.fixture(scope='module')
def new_role(app):
    role = Role(title='Operations Intern')
    return role


@pytest.fixture(scope='module')
def new_user(app, new_role):
    new_role.save()
    params = {
        'id': '1',
        'name': 'Ayo',
        'email': 'testemail@gmail.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id
    }
    user = User(**params)
    return user


@pytest.fixture(scope='module')
def new_asset_category(app):
    params = {'name': 'Laptop'}
    asset_category = AssetCategory(**params)
    return asset_category


@pytest.fixture(scope='module')
def test_asset_category(app):
    asset_category = AssetCategory(name='Laptop100')
    asset_category = asset_category.save()
    attribute_one = Attribute(
        _key='waranty',
        label='waranty',
        is_required=True,
        input_control='Text')
    attribute_two = Attribute(
        _key='length', label='length', is_required=False, input_control='Text')
    asset_category.attributes.append(attribute_one)
    asset_category.attributes.append(attribute_two)

    return asset_category


@pytest.fixture(scope='module')
def new_asset_category_with_non_deleted_asset(app):
    """
    The module scope is used here to prevent a test module data leaking into
    another.

    Fixture for asset category with a non deleted child asset.
    """

    asset_category = AssetCategory(name='Laptop0')
    asset_category = asset_category.save()

    asset = Asset(tag='abc', serial='def', asset_category_id=asset_category.id)

    asset = asset.save()

    return asset_category


@pytest.fixture(scope='module')
def new_asset_category_with_deleted_asset(app, request_ctx,
                                          mock_request_obj_decoded_token):
    """Fixture for asset category with a deleted child asset."""
    asset_category = AssetCategory(name='Laptop1')
    asset_category = asset_category.save()

    asset = Asset(tag='abd', serial='def', asset_category_id=asset_category.id)

    asset = asset.save()
    asset.delete()

    return asset_category


@pytest.fixture(scope='module')
def new_center(app):
    params = {'name': 'Lagos', 'image': {'url': 'image_url'}}
    center = Center(**params)
    return center


@pytest.fixture(scope='module')
def init_db(app):
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='module')
def auth_header(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }


@pytest.fixture(scope='module')
def auth_header_text(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE_TEXT,
        'Accept': MIMETYPE_TEXT
    }


@pytest.fixture(scope='module')
def request_ctx():
    """
    Setup a request client, this gets executed for each test module.

    :param app: Pytest fixture
    :return: Flask request client
    """
    ctx = current_app.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture(scope='module')
def mock_request_obj_decoded_token():
    """
    Mock decoded_token from request object
    """
    decoded_token = setattr(request, 'decoded_token',
                            {'UserInfo': {
                                'name': 'Ayobami'
                            }})

    return decoded_token


@pytest.fixture(scope='module')
def multiple_categories():
    """
    Create the asset category records for testing
    """
    categories = ['Laptop', 'Chromebook', 'Apple']

    for category in categories:
        db.session.add(AssetCategory(name=category))

    db.session.commit()


@pytest.fixture(scope='module')
def dynamic_filter():
    """
    Create the DynamicFilter object for testing
    """
    return DynamicFilter(AssetCategory)


@pytest.fixture(scope='function')
def test_center(app):
    """Create a center instance for testing"""
    center = Center(**VALID_CENTER_FOR_DELETE)

    center = center.save()
    yield center

    _db.session.delete(center)
    _db.session.commit()
