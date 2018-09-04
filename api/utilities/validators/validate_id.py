"""Module to validate resource id from url parameters"""

import re
from functools import wraps

from api.middlewares.base_validator import ValidationError
from ..messages.error_messages import serialization_errors


def is_valid_id(id_):
    """Check if id is valid"""
    return re.match('^[-a-zA-Z0-9_]*$', id_)


def validate_id(func):
    """Decorator function for views to validate id"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        for key in kwargs:
            if key.endswith('id') and not is_valid_id(kwargs.get(key, None)):
                raise ValidationError(
                    {
                        'status': 'error',
                        'message': serialization_errors['invalid_id']
                    }, 400)
        return func(*args, **kwargs)

    return decorated_function
