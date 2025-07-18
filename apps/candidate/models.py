from django.db import models

from libs.abstract.models import TimeStampedModel


# Candidate: Candidate profile
class Candidate(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Education: Education info for Candidate
class Education(TimeStampedModel):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.school} - {self.candidate.first_name} {self.candidate.last_name}"


# WorkExperience: Work experience info for Candidate
class WorkExperience(TimeStampedModel):
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.candidate.first_name} {self.candidate.last_name}"
