from functools import wraps
from flask import request, Response
import os

def check_auth(username, password):
    """Check if a username/password combo is valid."""
    return (
        username == os.environ.get("APP_USERNAME") and
        password == os.environ.get("APP_PASSWORD")
    )

def authenticate():
    """Send a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level.\n"
        "You have to login with proper credentials", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
