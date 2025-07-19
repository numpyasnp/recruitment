from django.contrib import admin

from .models import HRUser


@admin.register(HRUser)
class HrUserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "hr_company", "get_client_companies"]

    def get_client_companies(self, obj):
        return ", ".join([c.name for c in obj.client_companies.all()])

    get_client_companies.short_description = "Client Companies"
