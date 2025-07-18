from django.contrib import admin

from .models import HRCompany


@admin.register(HRCompany)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name"]
