from django.contrib import admin

from .models import CandidateFlow, Status, Activity, CandidateActivityLog


@admin.register(CandidateFlow)
class CandidateFlowAdmin(admin.ModelAdmin):
    list_select_related = ("job_posting", "candidate", "hr_user", "status")
    list_display = ["id", "job_posting", "candidate", "hr_user", "status"]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_select_related = ("candidate_flow", "created_by")
    list_display = ["id", "candidate_flow", "created_by", "status", "note"]


@admin.register(CandidateActivityLog)
class CandidateActivityLogAdmin(admin.ModelAdmin):
    list_select_related = ("candidate_flow", "activity", "status", "created_by")
    list_display = ["id", "candidate_flow", "activity", "status", "created_by", "note"]
