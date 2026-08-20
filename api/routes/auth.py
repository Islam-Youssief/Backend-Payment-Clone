
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
@require_authentication
def setup_2fa(user):
    return auth.setup_2fa(user)

@auth_api.route('/2fa/confirm', methods=["POST"])
@require_authentication
def confirm_2fa(user):
    data = fl.request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    code = data.get("code")

    if not code:
        return {
            "message": "Code is required"
        }, 400

    return auth.confirm_2fa(user, code)