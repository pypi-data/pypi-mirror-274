import logging
from kombu import Queue
from kombu import Exchange


def use_different_queue(app):
    """设置每个任务都使用不同的队列。"""
    logging.info("let CELERY use a different queue for each task...")
    # 处理没有task_routes预设置的情况
    if app.conf.task_routes is None:
        app.conf.task_routes = {}
    # 处理task_routes预设置为tuple的情况
    if isinstance(app.conf.task_routes, tuple):
        app.conf.task_routes = list(app.conf.task_routes)
        # 处理task_routes预设置为tuple但没有添加有效
        if len(app.conf.task_routes) < 1:
            app.conf.task_routes.append([])

    if app.conf.task_queues is None:
        app.conf.task_queues = []
    if isinstance(app.conf.task_queues, tuple):
        app.conf.task_queues = list(app.conf.task_queues)

    for task_name in app.tasks.keys():
        if task_name.startswith("celery."):
            continue

        if not task_name in app.conf.task_routes:
            if isinstance(app.conf.task_routes, dict):
                app.conf.task_routes.update(
                    {
                        task_name: {"queue": task_name},
                    }
                )
            else:
                app.conf.task_routes[0][0].append(
                    (task_name, {"queue": task_name}),
                )

        app.conf.task_queues.append(
            Queue(task_name, Exchange(task_name, type="direct"), routing_key=task_name),
        )
