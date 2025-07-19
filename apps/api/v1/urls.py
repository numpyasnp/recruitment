from django.urls import include, path


app_name = "v1"

urlpatterns = [
    path("", include("apps.api.v1.hr_user.urls")),
    path("auth/", include("apps.api.v1.auth.urls")),
    path("", include("apps.api.v1.job_posting.urls")),
    path("", include("apps.api.v1.candidate.urls")),
]
