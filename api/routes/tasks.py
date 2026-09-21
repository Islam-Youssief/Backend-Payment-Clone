import flask as fl

import api.controllers.tasks as tasks
from api.services.authentication.decorator import require_authentication
from api.services.permissions import PermissionService
tasks_api = fl.Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_api.route("/",methods=["GET"])
@require_authentication
def get_task(user):
    if not PermissionService.has_permission(user.id,"kanbanBoard_allowed"):
        return {
            "message": "You do not have permission to access the gallery"
        }, 403
    return tasks.TaskController.get_tasks(user.id)

@tasks_api.route("/",methods=["POST"])
@require_authentication
def create_task(user):
    if not PermissionService.has_permission(user.id,"kanbanBoard_allowed"):
            return {
                "message": "You do not have permission to access the gallery"
            }, 403
    data = fl.request.get_json() or {}

    name = data.get("name")
    description = data.get("description")
    status = data.get("status")
    if not name:
        return {
            "message" : "Task name is required"
        },400
    return tasks.TaskController.create_task(user.id,name,description,status)

@tasks_api.route("/<int:task_id>/status",methods = ["PATCH"])
@require_authentication
def update_task_status(user,task_id):
    if not PermissionService.has_permission(user.id,"kanbanBoard_allowed"):
            return {
                "message": "You do not have permission to access the gallery"
            }, 403
    data = fl.request.get_json() or {}

    status = data.get("status")

    if not status:
        return{
            "message" : "Status is required"
        },400

    return tasks.TaskController.update_task_status(user.id,task_id,status)

@tasks_api.route("/<int:task_id>",methods =["DELETE"])
@require_authentication
def delete_task(user,task_id):
    if not PermissionService.has_permission(user.id,"kanbanBoard_allowed"):
            return {
                "message": "You do not have permission to access the gallery"
            }, 403
    return tasks.TaskController.delete_task(user.id,task_id)