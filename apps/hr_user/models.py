from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany

from libs.abstract.models import TimeStampedModel


# HRUser: HR hr_user, linked to HRCompany and authorized ClientCompanies
class HRUser(AbstractUser, TimeStampedModel):
    hr_company = models.ForeignKey(HRCompany, on_delete=models.CASCADE, related_name="hr_users", null=True, blank=True)
    client_companies = models.ManyToManyField(ClientCompany, related_name="authorized_hr_users", blank=True)

    def __str__(self):
        return self.username
