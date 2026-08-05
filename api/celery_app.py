from celery import Celery
import api.core.configurations as configurations


def create_celery_app(app_config=None):
    config = app_config or configurations.AppConfig()
    celery = Celery(
        'api',
        broker=config.celery_broker_url,
        backend=config.celery_result_backend
    )
    celery.autodiscover_tasks(['api.tasks'])
    return celery

celery_app = create_celery_app()
