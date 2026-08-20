from api.models import User
from api.models import db


class AuthService:
    @staticmethod
    def verify_password(user,password):
        return user.check_password(password)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def authenticate(user, password):    
        if not user:
            return None
        if not user.check_password(password):
            return None

        return user

    @staticmethod
    def create_user(username,email,password):
        user = User(username=username,email=email,password=password)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user