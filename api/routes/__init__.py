import flask as fl

import api.routes.payments as payments
import api.routes.auth as auth
import api.routes.permissions as permissions
import api.routes.dashboard as dashboard
import api.routes.tasks as tasks
BLUEPRINTS = [
    payments.payments_api,auth.auth_api,permissions.permissions_api,
    dashboard.dashboard_api,tasks.tasks_api
]


def register_blueprints(app):
    api = fl.Blueprint('api', __name__, url_prefix='/api')
    for blueprint in BLUEPRINTS:
        api.register_blueprint(blueprint)
    app.register_blueprint(api)

