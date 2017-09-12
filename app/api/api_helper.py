import numbers

from flask import jsonify, request

from app import app
from app.util.exceptions import abort_request as abort
from app.util.exceptions import ERROR_LEVEL_VALIDATION

_number_types = [int, long, float]
_str_types = [str, unicode]


def enforce_param_existence(content, param_name):
    if param_name not in content:
        error_message = '%s is a required parameter.' % param_name
        error_content = {}
        error_content['missing_parameter'] = param_name
        abort(400, ERROR_LEVEL_VALIDATION, 0, error_content=error_content, error_message=error_message)


def enforce_param_type(content, param_name, param_type, is_json=True):
    if is_json:
        param = content[param_name]
    else:
        param = content.get(param_name, type=param_type)

    if param_type in _number_types:
        is_valid = isinstance(param, numbers.Number)
    elif param_type in _str_types:
        is_valid = isinstance(param, basestring)
    elif param_type == bool:
        is_valid = isinstance(param, param_type) or param == 0 or param == 1
    else:
        is_valid = isinstance(param, param_type)

    if not is_valid:
        error_message = '%s (%s) should be of type %s instead of type %s.' % (param_name, str(param), param_type, str(type(param)))
        error_content = {}
        error_content['parameter_name'] = param_name
        error_content['expected_type'] = str(param_type)
        abort(400, ERROR_LEVEL_VALIDATION, 1, error_content=error_content, error_message=error_message)


# guarantee both existence and type
def required_param(content, param_name, param_type, is_json=True):
    enforce_param_existence(content, param_name)
    enforce_param_type(content, param_name, param_type, is_json=is_json)

    if is_json:
        param = content[param_name]
    else:
        param = content.get(param_name, type=param_type)

    return param


# guarantee type, return None if does not exist
def optional_param(content, param_name, param_type, is_json=True):
    if is_json:
        if param_name in content:
            param = content[param_name]
        else:
            param = None
    else:
        param = content.get(param_name, type=param_type)

    if param:
        enforce_param_type(content, param_name, param_type, is_json)

    return param


# guarantee that none of the given param names have been sent, useful for debugging api issues
def prohibited_param_check(content, *param_names):
    if not app.debug:  # only perform the check in debug mode
        return
    for param_name in param_names:
        if param_name in content:
            error_message = 'The parameter "%s" is not allowed in this configuration. (Debug)' % (param_name)
            error_content = {}
            error_content['parameter_name'] = param_name
            abort(400, ERROR_LEVEL_VALIDATION, 2, error_content=error_content, error_message=error_message)


# validators is a function pointer. the function should take in the value and return True if the value passes validation, False otherwise
def validate_value(value, validator, error_message):
    if not validator(value):
        abort(400, ERROR_LEVEL_VALIDATION, 3, error_message=error_message)