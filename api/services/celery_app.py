from celery import Celery

app = Celery('my_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')


@app.task(name='my_app.send_notification')
def send_notification(payload):
   return f"status: {payload.get('status')}, message: {payload.get('message')}, payment_id: {payload.get('payment_id')}"