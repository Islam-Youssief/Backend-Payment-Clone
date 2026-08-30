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
    def get_user_by_id(user_id):
        return db.session.get(User, user_id)
    
    @staticmethod
    def get_user_by_phone(phone):
        return User.query.filter_by(phone=phone).first()
    
    @staticmethod
    def authenticate(user, password):    
        if not user:
            return None
        if not user.check_password(password):
            return None

        return user

    @staticmethod
    def create_user(username,email,password,phone):
        user = User(username=username,email=email,password=password,phone=phone)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_password(user,new_password):
        user.set_password(new_password)
        db.session.commit()