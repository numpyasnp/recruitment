from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model which adds creation and update timestamps"""

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if update_fields:
            update_fields = [*update_fields, "date_updated"]
        return super().save(force_insert, force_update, using, update_fields)


class PeriodMixin(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
