"""
Flask application factory for the Accounts & Payments Service API.
"""
import os

import flask as fl
from  api.extensions import limiter
import api.models as models
import api.routes as routes

def create_app(log_level, config_class=None):
    app = fl.Flask(__name__)
    app.logger.setLevel(log_level)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", 'sqlite:///db.sqlite3')
    models.db.init_app(app)
    models.migrate.init_app(app, models.db, render_as_batch=True)

    limiter.init_app(app)
    
    @app.errorhandler(429)
    def handle_rate_limit(e):
        return {
            "message":"Too many requests",
            "status":"rate_limited"
        },429
    
    routes.register_blueprints(app)
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    return app
