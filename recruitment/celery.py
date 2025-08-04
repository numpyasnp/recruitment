import os
from celery import Celery
from decouple import config
from django.conf import settings

from recruitment.celery_schedules import CELERYBEAT_SCHEDULE

# Django ayarlarını Celery için set et
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")

# Celery app oluştur
app = Celery("recruitment")

# Django ayarlarından Celery konfigürasyonunu yükle
app.config_from_object("django.conf:settings", namespace="CELERY")

# Redis broker ve backend ayarları
app.conf.update(
    broker_url=config("CELERY_BROKER_URL", default="redis://localhost:6379/0"),
    result_backend=config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0"),
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 min
    task_soft_time_limit=25 * 60,  # 25 min
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    worker_concurrency=2,
    worker_max_memory_per_child=150_000,
    ignore_task_result=True,
    beat_schedule=CELERYBEAT_SCHEDULE,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
