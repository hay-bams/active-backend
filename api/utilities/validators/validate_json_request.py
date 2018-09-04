"""Module to validate for json content type in request"""

from functools import wraps

from flask import request

from ..messages.error_messages import serialization_errors
from ...middlewares.base_validator import ValidationError


def validate_json_request(func):
    """Decorator function to check for json content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise ValidationError({
                'status': 'error',
                'message': serialization_errors['json_type_required']
            }, 400)
        return func(*args, **kwargs)
    return decorated_function
