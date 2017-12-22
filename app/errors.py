from . import app
from flask import jsonify

class TokenError(Exception):
	pass

@app.errorhandler(TokenError)
def handle_token_error(error):
    response = jsonify({'error':"Invalid Token"})
    response.status_code = 403
    return response