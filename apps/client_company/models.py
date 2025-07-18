from django.db import models

from libs.abstract.models import TimeStampedModel


# ClientCompany: Client company (Müşteri şirketi)
class ClientCompany(TimeStampedModel):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
