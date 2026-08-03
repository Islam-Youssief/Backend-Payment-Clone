import os
import logging
import dotenv
from api.app import create_app
from api.models import db, PaymentAttempt, Customer, User
from api.services.redis_service import RedisService

def before_scenario(context, scenario):
    """
    Clear the database before each scenario to prevent UniqueViolation errors 
    and ensure a clean state for every test.
    """
    dotenv.load_dotenv()
    app = create_app(logging.DEBUG)
    with app.app_context():
        db.session.query(PaymentAttempt).delete()
        db.session.query(Customer).delete()
        db.session.commit()
    redis_service = RedisService()
    redis_service.flush_pattern("rate_limit:*")
