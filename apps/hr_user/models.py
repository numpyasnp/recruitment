from django.db import models
from django.contrib.auth import get_user_model

from libs.abstract.models import TimeStampedModel


# HRUser: HR hr_user, linked to HRCompany and authorized ClientCompanies
class HRUser(TimeStampedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    hr_company = models.ForeignKey("hr_company.HRCompany", on_delete=models.CASCADE, related_name="hr_users")
    client_companies = models.ManyToManyField("client_company.ClientCompany", related_name="authorized_hr_users")

    def __str__(self):
        return f"{self.user.username}"
