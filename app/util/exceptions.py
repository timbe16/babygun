from werkzeug.exceptions import default_exceptions, HTTPException
from flask import make_response, request
from flask import abort as flask_abort
from flask import jsonify
from flask import url_for
import json

ERROR_LEVEL_AUTHENTICATION = 0
ERROR_LEVEL_VALIDATION = 1
ERROR_LEVEL_API = 2


class JSONHTTPException(HTTPException):
    """A base class for HTTP exceptions with ``Content-Type:
    application/json``.

    The ``description`` attribute of this class must set to a string (*not* an
    HTML string) which describes the error.

    """

    def get_body(self, environ):
        """Overrides :meth:`werkzeug.exceptions.HTTPException.get_body` to
        return the description of this error in JSON format instead of HTML.

        """
        return json.dumps(self.description)

    def get_headers(self, environ):
        """Returns a list of headers including ``Content-Type:
        application/json``.

        """
        return [('Content-Type', 'application/json')]


def _handle_error(status_code, error_content=None, error_message=None, headers=None):
    """
    Content for the error response.

    """

    if not headers:
        headers = {}

    content = {}

    content['status_code'] = status_code

    if error_message:
        content['error_message'] = error_message

    if error_content:
        content['error_content'] = error_content

    if 'text/html' in request.headers.get("Accept", ""):
        error_cls = HTTPException
    else:
        error_cls = JSONHTTPException

    class_name = error_cls.__name__
    bases = [error_cls]
    attributes = {'code': status_code}

    if status_code in default_exceptions:
        # Mixin the Werkzeug exception
        bases.insert(0, default_exceptions[status_code])

    error_cls = type(class_name, tuple(bases), attributes)
    flask_abort(make_response(error_cls(content), status_code, headers))


def abort_request(status_code, error_content=None, error_message=None, headers=None):
    _handle_error(status_code, error_content, error_message, headers)
