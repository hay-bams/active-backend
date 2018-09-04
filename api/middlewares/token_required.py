"""Module for token validation"""

from os import getenv as env
from functools import wraps
from base64 import b64decode

from flask import request
import jwt

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import jwt_errors


def token_required(function):
    """Authentication decorator. Validates token from the client"""

    @wraps(function)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        from .base_validator import ValidationError

        if not token:
            raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)

        elif 'bearer' not in token.lower():
            raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)

        try:
            token = token.split(' ')[-1]
            if env('FLASK_ENV') == 'testing':
                public_key = env('JWT_PUBLIC_KEY_TEST')
            elif env('FLASK_ENV') == 'production':
                public_key64 = env('JWT_PUBLIC_KEY')
                public_key = b64decode(public_key64).decode(CHARSET)
            else:
                public_key64 = env('JWT_PUBLIC_KEY_STAGING')
                public_key = b64decode(public_key64).decode(CHARSET)

            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                }
            )
        except ValueError as error:
            raise ValidationError({
                    'message': jwt_errors['SERVER_ERROR_MESSAGE']}, 500
                )
        
        except jwt.exceptions.InvalidAudienceError:
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience='andela.com',
                options={
                    'verify_signature': True,
                    'verify_exp': True
                }
            )

        except TypeError:
            raise ValidationError(
                    {'message': jwt_errors['SERVER_ERROR_MESSAGE']}, 500
                )

        except jwt.ExpiredSignatureError:
            raise ValidationError({'message': jwt_errors['EXPIRED_TOKEN_MSG']}, 401)

        except jwt.DecodeError as error:
            if str(error) == 'Signature verification failed':
                raise ValidationError(
                        {'message': jwt_errors['SIGNATURE_ERROR']}, 500
                    )

            else:
                raise ValidationError(
                        {'message': jwt_errors['INVALID_TOKEN_MSG']}, 401
                    )

        # setting the payload to the request object and can be accessed with \
        # request.decoded_token from the view
        setattr(request, 'decoded_token', decoded_token)
        return function(*args, **kwargs)

    return decorated_function
