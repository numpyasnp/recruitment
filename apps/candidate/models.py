from django.db import models
from django.utils.translation import gettext_lazy as _

from libs import customfields
from libs.abstract.models import TimeStampedModel, PeriodMixin
from libs.utils.general import split_name


class Candidate(TimeStampedModel):
    recruiter = models.ForeignKey("hr_user.HRUser", on_delete=models.DO_NOTHING, related_name="candidates")
    name = models.CharField(max_length=100, verbose_name=_("name and surname"), db_index=True)
    email = customfields.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        db_table = "candidate"

    @property
    def first_name(self):
        first_name, last_name = split_name(self.name)
        return first_name

    @property
    def last_name(self):
        first_name, last_name = split_name(self.name)
        return last_name


class Education(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255, db_index=True)
    department = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.department}"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        db_table = "education"


class WorkExperience(TimeStampedModel, PeriodMixin):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255, db_index=True)
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
