from api.services.authentication.auth import AuthService
from api.services.authentication.totp import TotpService
from api.services.authentication.token import TokenService

def register(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password :
        return {"message" : "Username,email,password are required!"},400

    if AuthService.get_user_by_email(email):
        return {"message" : "Email already exists"}

    if AuthService.get_user_by_username(username):
        return {"message" : "Username already exists"}
    
    user = AuthService.create_user(username,email,password)
    
    return {
        "messsage" : "User Created",
        "user_id" : user.id
        }, 201

def login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message":"Email and Password are requierd"
        },400
    
    user = AuthService.get_user_by_email(email)
    authenticated_user = AuthService.authenticate(user,password)

    if authenticated_user is None:
        return {
            "message":"Invalid credentials"
        },401
    access_token = TokenService.create_access_token(authenticated_user.id)
    return {
        "message" : "Authenticated",
        "access_token" : access_token
    },200

def setup_2fa(user):
    provisioning_uri = TotpService.setup(user)

    return {
        "provisioning_uri": provisioning_uri
    }, 200

def confirm_2fa(user, code):
    confirmed = TotpService.confirm(user, code)

    if not confirmed:
        return {
            "message": "Invalid authentication code"
        }, 401

    return {
        "message": "Two-factor authentication enabled"
    }, 200

def refresh(data):
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return {
            "message": "Refresh token is required"
        }, 400

    payload = TokenService.verify_refresh_token(
        refresh_token
    )

    if payload is None:
        return {
            "message": "Invalid or expired refresh token"
        }, 401

    user_id = int(payload["sub"])

    user = AuthService.get_user_by_id(user_id)

    if user is None:
        return {
            "message": "User not found"
        }, 401

    access_token = TokenService.create_access_token(
        user.id
    )

    return {
        "access_token": access_token
    }, 200