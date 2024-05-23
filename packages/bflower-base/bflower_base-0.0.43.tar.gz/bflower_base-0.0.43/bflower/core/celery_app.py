from celery import Celery  # type: ignore


def make_celery(app_name: str, config: str) -> Celery:
    celery_app = Celery(app_name)
    celery_app.config_from_object(config)
    celery_app.conf.task_routes = {"bflower.worker.tasks.*": {"queue": "bflower"}}
    return celery_app


celery_app = make_celery("bflower", "bflower.core.celeryconfig")
