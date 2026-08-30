from api.services.authentication.auth import AuthService
from api.services.authentication.totp import TotpService
from api.services.authentication.token import TokenService
from api.services.authentication.encryption import EncryptionService
from api.services.authentication.email import EmailService
from api.services.authentication.password_reset import PasswordResetService
from api.services.authentication.wasender import WaSenderService

def register(data):
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not username or not email or not password or not phone :
        return {"message" : "Username,email,password,phone are required!"},400

    if AuthService.get_user_by_email(email):
        return {"message" : "Email already exists"},400

    if AuthService.get_user_by_phone(phone):
        return {"message" : "Phone number already exists"},400

    if AuthService.get_user_by_username(username):
        return {"message" : "Username already exists"},400
    
    user = AuthService.create_user(username,email,password,phone)
    challenge_token = TokenService.create_2fa_challenge_token(user.id)
    return {
        "messsage" : "User Created",
        "user_id" : user.id,
        "challenge_token": challenge_token,
        "requires_2fa_setup": True
        }, 201

def login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required"
        }, 400

    user = AuthService.get_user_by_email(email)

    authenticated_user = AuthService.authenticate(user,password)

    if authenticated_user is None:
        return {
            "message": "Invalid credentials"
        }, 401

    challenge_token = TokenService.create_2fa_challenge_token(authenticated_user.id)

    if not authenticated_user.totp_enabled:
        return {
            "message": "Two-factor authentication setup required",
            "requires_2fa_setup": True,
            "challenge_token": challenge_token
        }, 200

    return {
        "message": "Two-factor authentication required",
        "requires_2fa": True,
        "challenge_token": challenge_token
    }, 200

def setup_2fa(user):
    provisioning_uri = TotpService.setup(user)
    secret = EncryptionService.decrypt(user.totp_secret)
    return {
        "provisioning_uri": provisioning_uri,
        "secret": secret
    }, 200

def confirm_2fa(user, otp):
    confirmed = TotpService.confirm(user, otp)

    if not confirmed:
        return {
            "message": "Invalid authentication otp"
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

    payload = TokenService.verify_refresh_token(refresh_token)

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

    access_token = TokenService.create_access_token(user.id)

    return {
        "access_token": access_token
    }, 200

def get_user_from_2fa_challenge(challenge_token):
    payload = TokenService.verify_2fa_challenge_token(
        challenge_token
    )

    if payload is None:
        return None

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        return None

    return AuthService.get_user_by_id(user_id)

def login_2fa(data):
    challenge_token = data.get("challenge_token")
    otp = data.get("code")

    if not challenge_token or not otp:
        return {
            "message": "Challenge token and otp are required"
        }, 400

    payload = TokenService.verify_2fa_challenge_token(
        challenge_token
    )

    if payload is None:
        return {
            "message": "Invalid or expired challenge"
        }, 401

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        return {
            "message": "Invalid challenge"
        }, 401

    user = AuthService.get_user_by_id(user_id)

    if user is None:
        return {
            "message": "User not found"
        }, 401

    if not user.totp_enabled:
        return {
            "message": "Two-factor authentication is not enabled"
        }, 400

    if not TotpService.verify(user, otp):
        return {
            "message": "Invalid authentication otp"
        }, 401

    access_token = TokenService.create_access_token(user.id)

    return {
        "message": "Authenticated",
        "access_token": access_token
    }, 200

def forgot_password(data):
    email = data.get("email")
    method = data.get("method")
    
    if not email:
        return { 
            "message" : "Email is required"
        }, 400

    if method not in ["email", "whatsapp"]:
        return {
            "message": "Method must be email or whatsapp"
        }, 400
    
    user = AuthService.get_user_by_email(email)

    if user is None:
        return {
            "message" : "User not found"
        }, 404

    if method == "whatsapp" and not user.phone:
        return {
            "message": "No phone number is registered for this account"
        }, 400
    
    otp = PasswordResetService.generate_otp()

    PasswordResetService.store_otp(email,otp)

    if method == "email":
     EmailService.send_password_reset_otp(email,otp)

    elif method == "whatsapp":
        WaSenderService.send_password_reset_otp(user.phone,otp)

    return {
        "message" : "Sent password reset OTP"
    }, 200

def verify_reset_otp(data):
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return { 
            "message" : "Email and OTP are required"
        },400

    user = AuthService.get_user_by_email(email)
    
    if user is None:
        return{
            "message" : "User not found"
        }, 404

    valid = PasswordResetService.verify_otp(email,otp)

    if not valid:
        return {
            "message" : "Invalid OTP"
        }, 401

    reset_token = TokenService.create_password_reset_token(user.id)

    return{
        "message" : "OTP verified",
        "reset_token" : reset_token
    }, 200

def reset_password(data):
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")
    confirm_new_password = data.get("confirm_new_password")

    payload = TokenService.verify_password_reset_token(reset_token)
    if payload is None:
        return {
            "message" : "Invalid or expired token"
        },401
    
    if not new_password or not confirm_new_password:
        return{
            "message" : "Both fields are required"
        },400
    
    if new_password != confirm_new_password :
        return {
            "message" : "Passwords doesn't match"
        },400

    try:
        user_id = int(payload["sub"])
    except (KeyError,ValueError,TypeError):
        return{
            "message" : "Invalid Token"
        }

    user = AuthService.get_user_by_id(user_id)

    if user is None:
        return{
            "message" : "User not found"
        }, 404

    AuthService.update_password(user,new_password)

    return{
        "message" : "Password reseted successfully"
    },200