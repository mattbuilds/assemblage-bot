"""This is where all error classes will be placed

They will be added to the flask errorhandler
"""

from flask import jsonify
from . import app

class TokenError(Exception):
    """Is thrown when a authentication error occurs"""
    pass

@app.errorhandler(TokenError)
def handle_token_error(error):
    """Used to handle the TokenError"""
    response = jsonify({'error':"Invalid Token"})
    response.status_code = 403
    return response
