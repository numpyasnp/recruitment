from django.db import models

from libs.abstract.models import TimeStampedModel


class JobPosting(TimeStampedModel):
    hr_company = models.ForeignKey("hr_company.HRCompany", on_delete=models.CASCADE, related_name="job_postings")
    client_company = models.ForeignKey(
        "client_company.ClientCompany", on_delete=models.CASCADE, related_name="job_postings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    closing_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.client_company.name})"
