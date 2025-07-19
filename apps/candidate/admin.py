from django.contrib import admin

from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone"]

    def get_client_companies(self, obj):
        return ", ".join([c.name for c in obj.client_companies.all()])

    get_client_companies.short_description = "Client Companies"
