from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, EducationViewSet, WorkExperienceViewSet

from django.urls import path, include


app_name = "candidate"

router = DefaultRouter()
router.register(r"candidates", CandidateViewSet, basename="candidate")
router.register(r"educations", EducationViewSet, basename="education")
router.register(r"work-experiences", WorkExperienceViewSet, basename="workexperience")

urlpatterns = [
    path("", include(router.urls)),
]
