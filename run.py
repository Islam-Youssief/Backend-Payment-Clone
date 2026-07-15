"""
Startup script for the Flask application.

This is the script referenced by the ``startup-script`` bolt task and by the
behave-restful functional tests, which expect the app on ``127.0.0.1:5000``.
"""
import os

import dotenv

import api.app as app
import api.core.configurations as config

dotenv.load_dotenv()
log_level = os.getenv('LOG_LEVEL', 'INFO')
application = app.create_app(log_level, config.AppConfig())



if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5000)