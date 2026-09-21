from api.models import Task, db

class TaskService:

    @staticmethod
    def get_user_tasks(user_id):
        return Task.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_task(task_id,user_id):
        return Task.query.filter_by(id=task_id,user_id=user_id).first()

    @staticmethod
    def create_task(user_id,name,description=None,status="todo"):
        task = Task(
            user_id = user_id,
            name = name,
            description = description,
            status = status
        )

        db.session.add(task)
        db.session.commit()

        return task

    @staticmethod
    def update_task_status(task_id,user_id,status):
        task = TaskService.get_task(task_id,user_id)
        
        if task.user_id != user_id:
            return None

        if status not in ["todo","inProgress","done"]:
            return None

        task.status = status

        if status == "inProgress" and task.started_at is None:
            task.started_at = db.func.now()

        if status == "done" and task.completed_at is None:
            task.completed_at = db.func.now()

        db.session.commit()

        return task

    @staticmethod
    def delete_task(task_id,user_id):
        task = TaskService.get_task(task_id,user_id)

        if not task:
            return False
       
        db.session.delete(task)
        db.session.commit()
        return True