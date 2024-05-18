# celery-debug

celery debug tasks.

## 安装

```shell
pip install celery-debug
```

## 输出的celery调试服务

- debug.ping
- debug.echo

## 启动

1. 在工作目录下创建`celeryconfig.py`，添加以下内容

    ```python
    worker_concurrency = 10
    worker_pool = "threads"
    broker_url = "redis://redis/0"
    result_backend = "redis://redis/1"
    accept_content = ["application/json"]
    task_serializer = "json"
    result_accept_content = ["application/json"]
    result_serializer = "json"
    timezone = "Asia/Shanghai"
    broker_connection_retry_on_startup = True
    # 额外新增的配置项
    # 配置后所有任务都使用不同的队列
    use_different_queue = True
    ```

2. 使用以下命令启动celery worker

    ```shell
    celery -A celery_debug:app worker -Q debug -l DEBUG
    ```

## 版本记录

### v0.1.0

- 版本首发。

### v0.1.1

- 提供配置项，快速让所有任务都使用不同的队列。
