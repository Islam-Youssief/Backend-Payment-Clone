import flask as fl

import api.controllers.permissions as permissions
from api.services.authentication.decorator import require_authentication

permissions_api = fl.Blueprint('permissions', __name__, url_prefix='/permissions')

@permissions_api.route("/",methods = ["GET"])
@require_authentication
def get_permissions(user):
    return permissions.PermissionController.get_permissions(user.id)