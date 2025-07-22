from rest_framework.routers import DefaultRouter
from .views import CandidateFlowViewSet
from django.urls import path, include

app_name = "flow"

router = DefaultRouter()
router.register(r"candidate-flows", CandidateFlowViewSet, basename="candidateflow")

urlpatterns = [
    path("", include(router.urls)),
]
