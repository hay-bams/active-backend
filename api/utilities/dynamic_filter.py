import re
from datetime import datetime, date, time

from flask import request
from sqlalchemy import func
from sqlalchemy.types import Unicode

from .filter_functions import (like, is_equal, less_than, not_equal,
                               greater_than, less_or_equal, greater_or_equal)
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import filter_errors


class DynamicFilter:
    """
    A class that returns filtered database records
    """

    def __init__(self, model):
        """
        Constructor to initialize an instance of the class.
        :param model: the model class that will be using the methods of
        this class
        """
        self.model = model
        self.query = model.query

    mapper = {
        'like': like,
        'eq': is_equal,
        'lt': less_than,
        'ne': not_equal,
        'gt': greater_than,
        'le': less_or_equal,
        'ge': greater_or_equal,
    }

    def validate_query(self, key, value, op):
        """
        Validate parameters passed to any endpoint for filtering.

        For filtering by delete the parameter should be a boolean
        For filtering by date the date should be a valid date
        The filter operator should be valid

        delete Example
        ==============
        Correct:
        http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
        deleted,eq,true

        Incorrect and will throw an error and return a response:
        http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
        deleted,eq,Invalid_delete_value

        date example
        =============
        Correct:
        http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
        created_at,eq,218-06-19 12:06:43.339809

        Incorrect and will throw an error and return a response:
        http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
        created_at,eq,invalid_date

        Invalid operator example
        ========================
        http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
        deleted,invalid_operator,true

        The essence of this is to validate parameters before making a call to
        the database, if the parameters are invalid then we dont make any
        database query which therefore improves perfomance
        """
        fields = [
            'deleted', 'created_at', 'updated_at', 'deleted_at', 'warranty'
        ]

        if op not in self.mapper:
            raise ValidationError(
                dict(message=filter_errors['INVALID_OPERATOR']))

        try:
            if key in fields:
                if key in ('created_at', 'updated_at', 'deleted_at',
                           'warranty'):
                    datetime.strptime(value, "%Y-%m-%d")
                elif key == 'deleted' and value not in ('true', 'false'):
                    raise ValidationError(
                        dict(
                            message=filter_errors['INVALID_DELETE_ATTRIBUTE']))
        except ValueError:
            raise ValidationError(
                dict(message=filter_errors['INVALID_DATE'].format(value)))

    def filter_query(self, args):
        """
        Returns filtered database entries.
        An example of filter_condition is: User._query('name,like,john').
        Apart from 'like', other comparators are
        eq(equal to), ne(not equal to), lt(less than), le(less than or equal
        to)
        gt(greater than), ge(greater than or equal to)
        :param filter_condition:
        :return: an array of filtered records
        """

        raw_filters = args.getlist('where')
        result = self.query

        for raw in raw_filters:
            try:
                key, op, value = raw.split(',', 3)
            except ValueError:
                raise ValidationError(
                    dict(message=filter_errors['INVALID_FILTER_FORMAT'].format(
                        raw)))

            self.validate_query(key, value, op)

            column = getattr(self.model, key, None)
            json_field = getattr(self.model, 'custom_attributes', None)
            db_filter = self.mapper.get(op)

            if not column and not json_field:
                raise ValidationError(
                    dict(message=filter_errors['INVALID_COLUMN'].format(key)))
            elif not column and json_field:
                result = result.filter(
                    db_filter(
                        self.model.custom_attributes[key].astext.cast(Unicode),
                        value))
            elif str(column.type) == 'DATETIME':
                result = result.filter(db_filter(func.date(column), value))
            else:
                result = result.filter(db_filter(column, value))

        return result
