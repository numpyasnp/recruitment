from django.db import models

from libs import customfields
from libs.abstract.models import TimeStampedModel, PeriodMixin


class Candidate(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = customfields.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Education(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.department}"


class WorkExperience(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company} - {self.candidate.first_name} {self.candidate.last_name}"
