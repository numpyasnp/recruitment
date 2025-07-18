from django.db import models

from libs.abstract import TimeStampedModel


# HRCompany: Human Resources company (İK şirketi)
class HRCompany(TimeStampedModel):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
