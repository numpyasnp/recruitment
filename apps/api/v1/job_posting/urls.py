from rest_framework.routers import DefaultRouter
from .views import JobPostingViewSet

from django.urls import path, include


app_name = "job_posting"

router = DefaultRouter()
router.register(r"job-postings", JobPostingViewSet, basename="jobposting")

urlpatterns = [
    path("", include(router.urls)),
]
