from django.contrib import admin

from apps.job_posting.models import JobPosting
from apps.candidate.models import Candidate
from apps.hr_user.models import HRUser
from .models import CandidateFlow, Status, Activity, CandidateFlowLog


@admin.register(CandidateFlow)
class CandidateFlowAdmin(admin.ModelAdmin):
    list_select_related = ("job_posting", "candidate", "hr_user", "status", "activity")
    list_display = ["id", "job_posting", "candidate", "hr_user", "status", "activity"]
    search_fields = [
        "job_posting__title",
        "candidate__name",
        "candidate__email",
        "candidate__phone",
        "candidate__work_experiences__company",
        "candidate__educations__school",
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.managed_by_user(request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "job_posting":
            kwargs["queryset"] = JobPosting.objects.filter(hr_user=request.user)
        if db_field.name == "candidate":
            kwargs["queryset"] = Candidate.objects.filter(hr_user=request.user)
        if db_field.name == "hr_user":
            kwargs["queryset"] = HRUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        changes = {}
        if change:
            old_obj = CandidateFlow.objects.get(pk=obj.pk)
            for field in ["status", "activity", "hr_user"]:
                old_value = getattr(old_obj, field)
                new_value = getattr(obj, field)
                if old_value != new_value:
                    changes[field] = {
                        "old": str(old_value),
                        "new": str(new_value),
                    }

        super().save_model(request, obj, form, change)

        CandidateFlowLog.objects.create(
            candidate_flow=obj,
            action="update" if change else "create",
            performed_by=request.user if hasattr(request.user, "hruser") else None,
            changes=changes if change else None,
        )

    def delete_model(self, request, obj):
        CandidateFlowLog.objects.create(
            candidate_flow=obj,
            action="delete",
            performed_by=request.user if hasattr(request.user, "hruser") else None,
            changes={
                "status": str(obj.status),
                "activity": str(obj.activity),
                "hr_user": str(obj.hr_user),
            },
        )
        super().delete_model(request, obj)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "note"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "note"]


@admin.register(CandidateFlowLog)
class CandidateFlowLogAdmin(admin.ModelAdmin):
    list_select_related = ("candidate_flow",)
    list_display = ["id", "candidate_flow", "get_hr_user", "get_client_company", "date_created"]

    @admin.display(description="client company")
    def get_client_company(self, obj):
        return obj.candidate_flow.job_posting.client_company

    @admin.display(description="hr user")
    def get_hr_user(self, obj):
        return obj.candidate_flow.hr_user
