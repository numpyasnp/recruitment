from django.contrib import admin

from .models import CandidateFlow, Status, Activity


@admin.register(CandidateFlow)
class CandidateFlowAdmin(admin.ModelAdmin):
    list_select_related = ("job_posting", "candidate", "hr_user", "status")
    list_display = ["id", "job_posting", "candidate", "hr_user", "status"]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_select_related = ("candidate_flow", "hr_user")
    list_display = ["id", "candidate_flow", "hr_user", "status", "note"]
