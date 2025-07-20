CELERYBEAT_SCHEDULE = {
    "deactivate-expired-job-postings": {
        "task": "apps.job_posting.tasks.DeactivateExpiredJobPostings",
        "schedule": 60,  # todo: fix 3min
    },
}
