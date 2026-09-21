"""
Flask application factory for the Accounts & Payments Service API.
"""
import os
from dotenv import load_dotenv
import flask as fl
import api.models as models
import api.routes as routes
from flask_cors import CORS
from api.extentions import sock
load_dotenv()
def create_app(log_level, config_class=None):
    app = fl.Flask(__name__)
    sock.init_app(app)
    app.logger.setLevel(log_level)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", 'sqlite:///db.sqlite3')
    CORS(app)
    models.db.init_app(app)
    models.migrate.init_app(app, models.db, render_as_batch=True)
    routes.register_blueprints(app)
    return app
