from celery import shared_task
from celery.app import app_or_default


@shared_task(name="debug.ping")
def ping():
    return "pong"


@shared_task(name="debug.echo")
def echo(msg):
    return msg


app = app_or_default()
if hasattr(app.conf, "use_different_queue"):
    if getattr(app.conf, "use_different_queue"):
        from .utils import use_different_queue

        use_different_queue(app)
