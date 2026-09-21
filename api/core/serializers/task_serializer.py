class TaskSerializer:

    @staticmethod
    def serialize(task):
        return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "status": task.status,
                "started_at": task.started_at,
                "completed_at": task.completed_at
        }