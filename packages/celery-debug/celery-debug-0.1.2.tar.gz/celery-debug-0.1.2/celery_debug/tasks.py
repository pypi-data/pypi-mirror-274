from celery import shared_task

__all__ = [
    "ping",
    "echo",
]


@shared_task(name="debug.ping")
def ping():
    return "pong"


@shared_task(name="debug.echo")
def echo(msg):
    return msg
