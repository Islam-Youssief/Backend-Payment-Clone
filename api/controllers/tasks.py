from api.services.tasks import TaskService
from api.core.serializers.task_serializer import TaskSerializer

class TaskController:

    @staticmethod
    def get_tasks(user_id):
        tasks = TaskService.get_user_tasks(user_id)

        return [TaskSerializer.serialize(task) for task in tasks], 200

    @staticmethod
    def create_task(user_id,name,description,status="todo"):
        task = TaskService.create_task(user_id,name,description,status)

        return TaskSerializer.serialize(task),200

    @staticmethod
    def update_task_status(user_id,task_id,status):
        task = TaskService.get_task(task_id,user_id)

        if not task:
            return {
                "message" : "Task not found"
            }, 404

        task = TaskService.update_task_status(task_id,user_id,status)

        if not task:
            return {
                "message" : "Invalid task status"
            },400

        return TaskSerializer.serialize(task),200

    @staticmethod
    def delete_task(user_id,task_id):
        task = TaskService.get_task(task_id,user_id)

        if not task:
            return {
                "message" : "Task not found"
            } , 404
        TaskService.delete_task(task_id,user_id)
        return {
            "message": "Task deleted successfully"
        }, 200