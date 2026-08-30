from celery import Celery
import core.configurations as config

celery_app = Celery(
    "notifications",broker=config.CeleryConfig().broker_url,
      backend=config.CeleryConfig().result_backend)

celery_app.conf.update(
    task_serializer=config.CeleryConfig().task_serializer,
    result_serializer=config.CeleryConfig().task_serializer,
    accept_content=[config.CeleryConfig().task_serializer],
    acks_late=config.CeleryConfig().task_acks_late,
    task_time_limit=config.CeleryConfig().task_time_limit,
    task_ignore_result=False,
    result_expires=3600,
    worker_concurrency=config.CeleryConfig().worker_concurrency,
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    worker_cancel_long_running_tasks_on_connection_loss=True,
)

celery_app.conf.task_default_queue = 'default'