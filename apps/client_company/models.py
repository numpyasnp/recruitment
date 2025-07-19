from django.db import models

from libs.abstract.models import TimeStampedModel


class ClientCompany(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client Company"
        verbose_name_plural = "Client Companies"
        db_table = "client_company"
