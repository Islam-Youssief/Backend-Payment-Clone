
import flask as fl

import api.controllers.auth as auth
from api.services.authentication.decorator import require_authentication

auth_api = fl.Blueprint('auth', __name__, url_prefix='/auth')

@auth_api.route('/register', methods=["POST"])
def register():
    data = fl.request.get_json()
    if not data:
        return {
            "message": "Request body is required"
        }, 400
    return auth.register(data)

@auth_api.route('/login',methods=["POST"])
def login():
    data = fl.request.get_json()
    if not data:
        return {
           "message": "Request body is required"
           }, 400
    return auth.login(data)

@auth_api.route('/refresh', methods=["POST"])
def refresh():
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400
    return auth.refresh(data)

@auth_api.route('/2fa/setup', methods=["POST"])
def setup_2fa():
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    challenge_token = data.get("challenge_token")

    if not challenge_token:
        return {
            "message": "Challenge token is required"
        }, 400

    user = auth.get_user_from_2fa_challenge(
        challenge_token
    )

    if user is None:
        return {
            "message": "Invalid or expired challenge"
        }, 401

    return auth.setup_2fa(user) 

@auth_api.route('/2fa/confirm', methods=["POST"])
def confirm_2fa():
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    challenge_token = data.get("challenge_token")
    code = data.get("code")

    if not challenge_token or not code:
        return {
            "message": "Challenge token and code are required"
        }, 400

    user = auth.get_user_from_2fa_challenge(
        challenge_token
    )

    if user is None:
        return {
            "message": "Invalid or expired challenge"
        }, 401

    return auth.confirm_2fa(user, code)

@auth_api.route('/login/2fa', methods=["POST"])
def login_2fa():
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    return auth.login_2fa(data)

@auth_api.route('/forgot_password', methods=["POST"])
def forgot_password():
    data = fl.request.get_json()

    if not data:
        return{
            "message" : "Request body is required"
        }, 400
    return auth.forgot_password(data)

@auth_api.route('/verify_reset_otp' , methods=["POST"])
def verify_reset_otp():
    data = fl.request.get_json()

    if not data:
        return{
            "message" : "Request body is required"
        },400
    
    return auth.verify_reset_otp(data)

@auth_api.route('/reset_password', methods=["POST"])
def reset_password():
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required or invalid JSON"
        }, 400

    return auth.reset_password(data)