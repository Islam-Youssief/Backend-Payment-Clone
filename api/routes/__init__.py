import flask as fl

import api.routes.payments as payments


BLUEPRINTS = [
    payments.payments_api,
]


def register_blueprints(app):
    api = fl.Blueprint('api', __name__, url_prefix='/api')
    for blueprint in BLUEPRINTS:
        api.register_blueprint(blueprint)
    app.register_blueprint(api)

