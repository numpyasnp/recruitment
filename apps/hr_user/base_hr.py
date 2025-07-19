from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BaseHRQuerySet(QuerySet):
    @transaction.atomic
    def create_user(self, email: str, name: str, last_name: str, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not name or not last_name:
            raise ValueError("User must have a name and last name")

        user = self.create(email=email, name=name, last_name=last_name)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name: str, last_name: str):
        user = self.create_user(email, password=password, name=name, last_name=last_name)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseHRManager(BaseManager.from_queryset(BaseHRQuerySet), BaseUserManager):
    pass
