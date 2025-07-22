from django.contrib import admin

from .models import CandidateFlow, Status, Activity, CandidateActivityLog


@admin.register(CandidateFlow)
class CandidateFlowAdmin(admin.ModelAdmin):
    list_select_related = ("job_posting", "candidate", "hr_user", "status")
    list_display = ["id", "job_posting", "candidate", "hr_user", "status"]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "note"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "note"]


@admin.register(CandidateActivityLog)
class CandidateActivityLogAdmin(admin.ModelAdmin):
    list_select_related = ("candidate_flow", "activity")
    list_display = ["id", "candidate_flow", "get_hr_user", "get_client_company", "activity", "note", "date_created"]

    @admin.display(description="client company")
    def get_client_company(self, obj):
        return obj.candidate_flow.job_posting.client_company

    @admin.display(description="hr user")
    def get_hr_user(self, obj):
        return obj.candidate_flow.hr_user
