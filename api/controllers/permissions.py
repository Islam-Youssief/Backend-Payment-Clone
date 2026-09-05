from api.services.permissions import PermissionService


class PermissionController:
    @staticmethod
    def get_permissions(user_id):
        permissions = PermissionService.get_user_permission(user_id)

        return {
            "permissions" : permissions
        },200