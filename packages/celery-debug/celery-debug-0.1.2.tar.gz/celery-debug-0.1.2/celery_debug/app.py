from celery.app import app_or_default
from .utils import use_different_queue
from .tasks import *

app = app_or_default()
if hasattr(app.conf, "use_different_queue"):
    if getattr(app.conf, "use_different_queue"):
        use_different_queue(app)
