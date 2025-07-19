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

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        db_table = "candidate"


class Education(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.department}"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        db_table = "education"


class WorkExperience(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    tech_stack = models.TextField(
        blank=True, help_text="List of the technologies stack, separated by comma e.g Python, Django, PostgreSQL"
    )

    def __str__(self):
        return f"{self.company} - {self.candidate.first_name} {self.candidate.last_name}"

    class Meta:
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"
        db_table = "work_experience"
