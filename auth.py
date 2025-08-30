from functools import wraps
from flask import request, Response
import os

# Get credentials from environment variables
USERNAME = os.environ.get("BASIC_AUTH_USERNAME", "admin")
PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD", "password")

def check_auth(username, password):
    """Check if a username/password combo is valid."""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Send a 401 response that enables basic auth"""
    return Response(
        "🚫 Access Denied: Please provide valid credentials.\n", 
        401,
        {"WWW-Authenticate": 'Basic realm="FeeTrack Login"'}
    )

def requires_auth(f):
    """Decorator to enforce basic authentication on routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
