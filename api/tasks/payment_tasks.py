import logging
from api.celery_app import celery_app


@celery_app.task(name='send_payment_notification')
def send_payment_notification(payment_data):
    """Send notification after payment status is finalized via webhook."""
    logging.info(
        f"Payment notification: {payment_data['status']} - "
        f"Amount: {payment_data['amount']} {payment_data['currency']} - "
        f"Customer: {payment_data['customer_email']}"
    )
    return {'status': 'sent', 'payment_id': payment_data.get('payment_id')}
