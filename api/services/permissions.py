from api.models import UserPermission


class PermissionService:

    @staticmethod
    def get_user_permission(user_id):
        user_permissions = UserPermission.query.filter_by(user_id=user_id).all()
        return [
            user_permission.permission.name
            for user_permission in user_permissions
        ]

    @staticmethod
    def has_permission(user_id, permission_name):
        user_permissions = UserPermission.query.filter_by(user_id=user_id).all()

        return any(
            user_permission.permission.name == permission_name
            for user_permission in user_permissions
        )