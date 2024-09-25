from functools import wraps
from flask import request,jsonify,current_app
import jwt
import time
import os
def generate_token(user_name):
    payload = {
        "name": user_name,
        "exp": time.time() + 200   
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
         
        if not auth_header or not auth_header.startswith('Bearer '):
           
            return {'status_code': '401', 'message': 'Token is missing or malformed'}, 401
        
        token = auth_header[len('Bearer '):].strip()

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_name = payload['name']   
        except jwt.ExpiredSignatureError:
            return {'status_code': '401', 'message': 'Token is expired'}, 401
        except jwt.InvalidTokenError:
            return {'status_code': '401', 'message': 'Token is invalid'}, 401
        
        return f(*args, **kwargs)

    return decorated_function
def response(status_code, message, token=None, details=None):
    response_data = {
        'status_code': status_code,
        'message': message
    }

    if token is not None:
        response_data['token'] = token

     
    if details is not None:
        response_data['details'] = details
    return jsonify(response_data)

class HTTPStatusCode:
    PROCESSING = 102,
    EARLY_HINTS = 103
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500

    

    

