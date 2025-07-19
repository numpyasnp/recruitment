from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BaseHRQuerySet(QuerySet):
    @transaction.atomic
    def create_user(self, email: str, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.create(email=email, password=password)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseHRManager(BaseManager.from_queryset(BaseHRQuerySet), BaseUserManager):
    pass
