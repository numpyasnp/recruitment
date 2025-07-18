from django.contrib import admin

from .models import HRUser


@admin.register(HRUser)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["username"]
