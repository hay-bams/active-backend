""" Module with user model schemas. """
import re
from marshmallow import (ValidationError, fields, post_load)

from api.models.user import User
from ..validators.name_validator import name_validator
from ..validators.string_length_validators import string_length_60_validator
from ..messages.error_messages import serialization_errors
from .base_schemas import BaseSchema

email_regex = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def email_exists_validator(data):
    """
    Checks if given email has correct email syntax & not
    registered already. Raises a ValidationError otherwise
    """

    if not re.match(email_regex, data):
        raise ValidationError(
            serialization_errors['email_syntax'].format(data))
    elif User.query.filter_by(email=data).first():
        raise ValidationError(
            serialization_errors['email_exists'].format(data))
    else:
        raise ValidationError(serialization_errors['email_length'])


class UserSchema(BaseSchema):
    """ User model schema. """

    name = fields.String(required=True,
                         validate=(string_length_60_validator,
                                   name_validator),
                         error_messages={
                             'required':
                             serialization_errors['field_required']})
    email = fields.String(required=True,
                          validate=email_exists_validator,
                          error_messages={
                              'required':
                              serialization_errors['field_required']})
    image_url = fields.String()

    @post_load
    def create_user(self, data):
        """ Return user object after successful loading of data"""

        return User(**data)
