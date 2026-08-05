from celery import Celery

celery = Celery(
    "payment_service",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)

celery.conf.imports = ("api.tasks",)