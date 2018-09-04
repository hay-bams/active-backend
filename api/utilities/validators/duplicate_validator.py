"""Module for validating duplicate data"""
import re

from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import serialization_errors


def validate_duplicate(model, **kwargs):
    """
    Checks if model instance already exists in database

    Parameters:
         model(object): model to run validation on
         kwargs(dict): keyword arguments containing fields to filter query by
    """

    result = model.query.filter_by(deleted=False, **kwargs).first()
    if result:
        raise ValidationError({
            'message':
            serialization_errors['exists'].format(
                f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , model.__name__)}'
            )
        }, 409)
