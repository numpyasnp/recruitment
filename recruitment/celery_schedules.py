from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "deactivate-expired-job-postings": {
        "task": "apps.job_posting.tasks.DeactivateExpiredJobPostings",
        "schedule": crontab(minute="*/3"),  # every 3 min.
    },
}
