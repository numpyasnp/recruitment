from django.contrib import admin

from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_select_related = ("hr_user", "client_company", "hr_company")

    list_display = [
        "id",
        "hr_user",
        "hr_company",
        "client_company",
        "title",
        "description",
        "closing_date",
        "is_active",
    ]
