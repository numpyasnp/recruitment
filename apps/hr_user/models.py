from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.manager import BaseManager
from django.utils.translation import gettext_lazy as _

from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany
from apps.hr_user.base_hr import BaseHRManager
from apps.hr_user.base_hr import BaseHRQuerySet
from libs import customfields
from libs.abstract.models import TimeStampedModel


class HRUserQuerySet(BaseHRQuerySet):
    def active(self):
        return self.filter(is_active=True)


class HRUserManager(BaseManager.from_queryset(HRUserQuerySet), BaseHRManager):
    pass


class HRUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    USERNAME_FIELD = "email"

    hr_company = models.ForeignKey(HRCompany, on_delete=models.CASCADE, related_name="hr_users", null=True, blank=True)
    client_companies = models.ManyToManyField(ClientCompany, related_name="authorized_hr_users", blank=True)
    name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    email = customfields.EmailField(
        max_length=254,
        unique=True,
        error_messages={"unique": _("Email already exist")},
        verbose_name=_("email address"),
    )
    is_staff = property(lambda self: self.is_superuser)
    is_admin = property(lambda self: self.is_superuser)

    objects = HRUserManager()

    def __str__(self):
        return self.name
