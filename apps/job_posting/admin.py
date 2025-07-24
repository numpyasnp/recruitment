from django.contrib import admin

from apps.hr_user.models import HRUser
from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hr_user":
            kwargs["queryset"] = HRUser.objects.filter(id=request.user.id)
        if db_field.name == "hr_company":
            kwargs["queryset"] = HRCompany.objects.filter(hr_users=request.user)
        if db_field.name == "client_company":
            kwargs["queryset"] = ClientCompany.objects.filter(authorized_hr_users=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
