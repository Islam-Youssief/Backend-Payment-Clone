from api.models import User
from api.core.permissions import permissions,permissions_ids

class PermissionService:

    @staticmethod
    def get_user_permission(user_id):
        user = User.query.get(user_id)

        if not user.permissions:
            return []
        
        return [permissions[int(permission_id)] for permission_id in user.permissions.split(".")]

    @staticmethod
    def has_permission(user_id,permission_name):
        user = User.query.get(user_id)

        if not user.permissions:
            return False

        permission_id = permissions_ids.get(permission_name)

        if permission_id is None:
            return False
        user_permissions_ids = {int(permission_id) for permission_id in user.permissions.split(".")}

        return permission_id in user_permissions_ids

