""" Module holding all error messages, facilitates DRY principle"""

# Group errors by field type, generic messages go under field_{}
serialization_errors = {  #pylint: disable=C0103
    'email_syntax':
    '{0} is not a valid email address',
    'email_exists':
    '{0} is already registered',
    'email_length':
    'Email must be at least 6 characters',
    'field_required':
    'This field is required',
    'field_length':
    'Field must be at least {0} characters',
    'json_invalid':
    'Invalid JSON input provided',
    'string_characters':
    'Field must start and end with a letter, only contain letters, non-consecutive fullstops, hyphens, spaces and apostrophes',  #pylint: disable=C0301
    'string_length':
    'Field must be {0} characters or less',
    'input_control':
    'Incorrect input control type provided, please provide one of {input_controls}',  #pylint: disable=C0301
    'choices_required':
    'choices seperated by comma must be provided if multi choice inputs controls are selected',  #pylint: disable=C0301
    'provide_attributes':
    'Please provide at least one attribute',
    'attribute_required':
    'The attribute {} is required',
    'unrelated_attribute':
    'The attribute {} is not related to this asset category',
    'invalid_category_id':
    'This asset category id is invalid',
    'category_not_found':
    'This category does not exist in the database',
    'attribute_not_related':
    'attribute with the id of {attribute_id} is not related to the asset category of id {asset_category_id}',  #pylint: disable=C0301
    'invalid_id':
    'Invalid id in parameter',
    'key_error':
    '{} key not found',
    'choices_type':
    'Choices must be an Array',
    'invalid_field':
    'invalid field supplied',
    'invalid_query_strings':
    '{0} contains invalid parameter {1}',
    'json_type_required':
    'Content-Type should be application/json',
    'duplicate_asset':
    'Asset with the tag {} already exists',
    'asset_category_assets':
    'Assets for category {} fetched successfully',
    'exists':
    '{} already exists',
    'person_not_found':
    'Person not found',
    'last_page_returned':
    'The requested page exceeds the total pages count, however the last page was returned',
    'not_found':
    '{} not found'
}
jwt_errors = {
    'INVALID_TOKEN_MSG':
    "Authorization failed due to an Invalid token.",
    'EXPIRED_TOKEN_MSG':
    "Token expired. Please login to get a new token",
    'SIGNATURE_ERROR':
    "Cannot verify the signature of the token provided as\
 it was signed by a non matching private key",
    'SERVER_ERROR_MESSAGE':
    "Authorization failed. Please contact support.",
    'NO_BEARER_MSG':
    "Bad request. The token should begin with the word\
 'Bearer'.",
    'NO_TOKEN_MSG':
    "Bad request. Header does not contain an authorization\
 token.",
}
database_errors = {
    'model_delete_children': 'Delete failed. {0} has {1} not deleted.'
}

filter_errors = {
    'INVALID_DELETE_ATTRIBUTE':
    'deleted should be of type bool',
    'INVALID_DATE':
    'Invalid datetime format {}, date should be in this format\
: Y-M-D',
    'INVALID_OPERATOR':
    '''invalid operator, valid operators are \
'like, eq, lt, ne, gt, le, ge' ''',
    'INVALID_COLUMN':
    'Invalid filter column: {}',
    'INVALID_FILTER_FORMAT':
    'Invalid filter format: \'{}\'.'
}
