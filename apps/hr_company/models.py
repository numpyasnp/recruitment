from django.db import models

from libs.abstract.models import TimeStampedModel


class HRCompany(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
