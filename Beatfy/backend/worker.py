from celery import Celery
from flask import current_app as app

celery = Celery("Application Batch Jobs")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        
CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"

celery.conf.update(
    timezone="Asia/Kolkata",
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND
)

celery.Task = ContextTask