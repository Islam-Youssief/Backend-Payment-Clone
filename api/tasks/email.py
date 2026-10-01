from api.celery_app import celery


@celery.task
def send_receipt_email(email, payment_id, amount):
    print(
        f"Sending receipt email to {email} "
        f"for payment {payment_id} amount {amount}"
    )

    return {
        "status": "success",
        "message": "Receipt email sent"
    }