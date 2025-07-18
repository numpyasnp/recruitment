from rest_framework.routers import DefaultRouter
from .views import HRUserViewSet

from django.urls import path, include


app_name = "hr_user"

router = DefaultRouter()
router.register(r"hr-users", HRUserViewSet, basename="hruser")

urlpatterns = [
    path("", include(router.urls)),
]
