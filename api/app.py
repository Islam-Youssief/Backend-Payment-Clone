"""
Flask application factory for the Accounts & Payments Service API.
"""
import os

import flask as fl
import api.models as models
import api.routes as routes
from api.core.extentions import limiter

def create_app(log_level, config_class=None):
    app = fl.Flask(__name__)
    app.logger.setLevel(log_level)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", 'sqlite:///db.sqlite3')
    app.config["RATELIMIT_STORAGE_URI"] = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    app.config["RATELIMIT_DEFAULT"] = "200 per day;50 per hour"
    limiter.init_app(app)
    models.db.init_app(app)
    models.migrate.init_app(app, models.db, render_as_batch=True)
    routes.register_blueprints(app)
    return app
