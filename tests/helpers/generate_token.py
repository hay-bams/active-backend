"""Module for token generation"""

from os import getenv
from datetime import datetime
from base64 import b64encode, b64decode, encode

import jwt

from ..mocks.user import user_one
from api.utilities.constants import CHARSET


def generate_token(exp=None):
    """
    Generates jwt tokens for testing purpose

    params:
        exp: Token Expiration. This could be datetime object or an integer
    result:
        token: This is the bearer token in this format 'Bearer token'
    """

    secret_key = getenv('JWT_SECRET_KEY')
    payload = {'UserInfo': user_one.to_dict()}
    payload.__setitem__('exp', exp) if exp is not None else ''
    token = jwt.encode(payload, secret_key, algorithm='RS256').decode(CHARSET)
    return 'Bearer {0}'.format(token)