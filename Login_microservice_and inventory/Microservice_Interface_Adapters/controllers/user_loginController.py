from flask import Blueprint, request
import logging
from Microservice_Entities.loginentities import LoginRequest
from Microservice_frameworks_drivers.utils import response, generate_token, token_required
from Microservice_frameworks_drivers.service import authenticate_user, get_user_details
bp = Blueprint('api', __name__)
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return response("400", "Empty request body", None), 400
    if 'user_name' not in data or 'user_password' not in data:
        return response("400", "bad request", None), 400
    try:
        login_request = LoginRequest(**data)
        user_name = login_request.user_name
        user_password = login_request.user_password
        if not user_name:
            return response("102", "Required username", None)
        if not user_password:
            return response("102", "Required password", None)
        
        auth_result = authenticate_user(user_name, user_password)
        if auth_result.json['status_code'] == "200":
            token = generate_token(user_name)
            return response(auth_result.json['status_code'], auth_result.json['message'], token)
        else:
            return response(auth_result.json['status_code'], auth_result.json['message'])
    except Exception as e:
        logging.error('An exception occurred during login: %s', e)
        return response("500", "Internal Server Error", None), 500

@bp.route('/inventory', methods=['GET'])
@token_required
def get_inventory():
    user_name = request.user_name  
    try:
        details_result = get_user_details(user_name)
        if details_result.json['status_code'] == "200":
            return response(details_result.json['status_code'], details_result.json['message'], None,details_result.json['details'])
        else:
            return response(details_result['status_code'], details_result['message'],None,None)
    except Exception as e:
        logging.error('An exception occurred while fetching user details: %s', e)
        return response("500", "Internal Server Error", None), 500
