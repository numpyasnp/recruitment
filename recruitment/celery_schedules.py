from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "deactivate-expired-job-postings": {
        "task": "apps.job_posting.tasks.DeactivateExpiredJobPostings",
        "schedule": crontab(minute="*/3"),  # every 3 min.
    },
    "monthly_activity_report_pdf": {
        "task": "apps.flow.tasks.MonthlyActivityReportPdf",
        "schedule": crontab(minute=5, hour=0, day_of_month=1),
    },
    "weekly_activity_report_pdf": {
        "task": "apps.flow.tasks.WeeklyActivityReportPdf",
        "schedule": crontab(minute=59, hour=23, day_of_week=6),
    },
}
