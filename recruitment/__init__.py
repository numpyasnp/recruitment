# Celery app'i Django başlatılırken yükle
from .celery import app as celery_app

__all__ = ("celery_app",)
