from django.contrib import admin

from .models import Candidate, Education, WorkExperience


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "hr_user", "name", "email", "phone"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("hr_user")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_select_related = ["candidate"]
    list_display = ["id", "candidate", "department"]


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_select_related = ["candidate"]
    list_display = ["id", "candidate", "company", "position"]
