"""Module for pagination helpers"""

from functools import wraps
from math import ceil
from werkzeug.datastructures import ImmutableMultiDict
import re

from flask import request

from .messages.error_messages import serialization_errors
from ..middlewares.base_validator import ValidationError
from .constants import EXCLUDED_FIELDS


def validate_pagination_args(arg_value, arg_name):
    """
    Validates if the query strings are valid.

    Arguments:
        arg_value (string): Query string value
        arg_name (string): Query string name

    Raises:
        ValidationError: Use to raise exception if any error occur

    Returns:
        (int) -- Returns True or False
    """

    if arg_name == 'limit' and arg_value == 'None':
        return 10  # Defaults limit to 10 if not provided
    if arg_name == 'page' and arg_value == 'None':
        return 1  # Defaults page to 1 if not provided

    # Checks if the arg is >= 1
    if arg_value.isdigit() and int(arg_value) > 0:
        return int(arg_value)
    else:
        raise ValidationError({
            'message':
            serialization_errors['invalid_query_strings'].format(
                arg_name, arg_value)
        })


def pagination_helper(model, schema, extra_query=None):
    """
    Paginates records of a model.
    
    Arguments:
        model (class): Model to be paginated
        schema (class) -- Schema to be used for serilization
    
    Keyword Arguments:
        extra_query (dict): Contains extra query to be performed on the model
                            (default: {None})

        example: {"asset_category_id": "-LHYVNP2yx8oIOJFzXS4", "deleted": False}
    
    Returns:
        (tuple): Returns a tuple containing the paginated data and the 
                paginated meta object or returns a tuple of None depending on 
                whether the limit and page object is provided
    """

    # Validates if the query strings are digits and the digits are >= 1
    limit = validate_pagination_args(
        request.args.get('limit', 'None'), 'limit')
    current_page_count = validate_pagination_args(
        request.args.get('page', 'None'), 'page'
    )  # assign the page query string to the variable current_page_count

    query = model._query(request.args)

    # Removes the trailing / at the end of the root url
    root_url = request.url_root[:-1]
    # Removes the trailing / at the begining of the url path
    url_path = request.path[1:]
    base_url = f'{root_url}/{url_path}'
    current_page_url = request.url

    records_query = query.filter_by(deleted=False)

    # Checks if they are extra queries to perform on the model
    if extra_query and isinstance(extra_query, dict):
        try:
            records_query = records_query.filter_by(**extra_query)
        except:
            # Raise a validation error if the keys in the extra queries are not part of the models fields
            raise ValidationError({
                'message':
                serialization_errors['invalid_field']
            })

    records_count = records_query.count()
    first_page = f'{base_url}?page=1&limit={limit}'
    pages_count = ceil(records_count / limit)

    meta_message = None

    if current_page_count > pages_count:
        # If current current_page_count > pages_count set current_page_count to pages_count
        current_page_count = pages_count
        first_page = f'{base_url}?page=1&limit={limit}'
        current_page_url = f'{base_url}?page={pages_count}&limit={limit}'
        meta_message = serialization_errors['last_page_returned']

    offset = (current_page_count - 1) * limit

    records = records_query.offset(offset).limit(limit)

    # pagination meta object
    pagination_object = {
        "firstPage": first_page,
        "currentPage": current_page_url,
        "nextPage": "",
        "previousPage": "",
        "page": current_page_count,
        "pagesCount": pages_count,
        "totalCount": records_count
    }

    previous_page_count = current_page_count - 1
    next_page_count = current_page_count + 1

    next_page_url = f'{base_url}?page={next_page_count}&limit={limit}'
    previous_page_url = f'{base_url}?page={previous_page_count}&limit={limit}'  # noqa

    if current_page_count > 1:
        # if current_page_count > 1 there should be a previous page url
        pagination_object['previousPage'] = previous_page_url

    if pages_count >= next_page_count:
        # if pages_count >= next_page_count there should be a next page url
        pagination_object['nextPage'] = next_page_url

    if meta_message:
        pagination_object['message'] = meta_message

    data = schema(many=True, exclude=EXCLUDED_FIELDS).dump(records).data

    return data, pagination_object
