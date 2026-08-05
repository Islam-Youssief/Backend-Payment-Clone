from api.celery_app import celery

@celery.task
def send_webhook(payment):
    print(f"Sending webhook: {payment}")

    return {
        "status": "sent"
    }