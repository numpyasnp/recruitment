from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BaseHRQuerySet(QuerySet):
    @transaction.atomic
    def create_user(self, email: str, password: str, name: str = "", last_name: str = ""):
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Password may not blank")

        user = self.create(email=email, password=password, name=name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, name: str, last_name: str):
        user = self.create_user(email, password=password, name=name, last_name=last_name)
        user.is_superuser = True
        user.save()
        return user


class BaseHRManager(BaseManager.from_queryset(BaseHRQuerySet), BaseUserManager):
    pass
