from functools import wraps
from .exceptions import *
from app import app


@app.before_request
def before_request():
    client_key = request.headers.get('Client-Key', None)
    if not client_key or (client_key != app.config['CLIENT_KEY']):
        abort_request(401, ERROR_LEVEL_AUTHENTICATION, 0, error_message="Invalid client key.")


def auth_token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        # tbd: check unique auth token for each user
        token_string = request.headers.get('Authentication-Token', None)
        return fn(*args, **kwargs)

    return decorated
