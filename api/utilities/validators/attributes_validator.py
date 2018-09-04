"""Module for AttributeSchema validation """

from marshmallow import ValidationError as MarshError
from flask import request

from api.utilities.enums import InputControlChoiceEnum
from api.models.asset_category import AssetCategory
from ..validators.validate_id import is_valid_id
from ..messages.error_messages import serialization_errors


def validate_choices_after_dump(data):
    """ 
    Checks if choices should be returned to the client.

    if the input control is not a multi-choice type,
    then the choices are not returned to the client,
    else the choices is converted into an array and returned to the client

    (data)dict: attributes data

    Returns: None
    """

    if not data['choices'] or data['choices'] == ['']:
        del data['choices']
    else:
        data['choices'] = data['choices'][0].split(',')


def validate_attribute_exists(attribute_id):
    """
    Validates if attribute is related to an asset category that its id matches
    the id provided in the url
    """

    try:
        asset_category_id = request.url.split('/').pop()
        if is_valid_id(attribute_id):
            attribute = AssetCategory.get(
                asset_category_id).attributes.filter_by(
                    id=attribute_id).first()

            if not attribute:
                raise Exception('attribute not found')
        else:
            raise Exception('missing value')
    except:
        raise MarshError(serialization_errors['attribute_not_related'].format(
            attribute_id=attribute_id, asset_category_id=asset_category_id))


def remove_duplicate(choices):
    """
    Remove duplicates from choices
    """

    unique_choices = []
    for choice in choices:
        if choice and choice.lower() not in unique_choices:
            unique_choices.append(choice.lower())

    return unique_choices


def validate_choices(data):
    """
    Validates if choices is required or not
    """
    input_control = data.get('input_control', '').lower()

    choices = data.get('choices', [])

    if type(choices) is not list:
        raise MarshError(serialization_errors['choices_type'], 'choices')

    choices = ','.join(remove_duplicate(choices))
    multi_choices = InputControlChoiceEnum.get_multichoice_fields()
    single_choices = InputControlChoiceEnum.get_singlechoice_fields()
    data['choices'] = choices

    # Raises an Exception if input_control is a multichoice and choices are empty
    if input_control in multi_choices and not choices:  # pylint: disable=C0301
        raise MarshError(serialization_errors['choices_required'], 'choices')

    # Raises an Exception if input_control is not a multichoice
    if input_control in single_choices and choices:  # pylint: disable=C0301
        del data['choices']
