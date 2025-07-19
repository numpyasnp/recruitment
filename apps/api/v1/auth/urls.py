from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api.v1.auth.views import HRSessionLoginView, HRSessionLogoutView

app_name = "auth"


urlpatterns = [
    # Session Based
    path("login/session", HRSessionLoginView.as_view(), name="login"),
    path("logout/session", HRSessionLogoutView.as_view(), name="logout"),
    # Jwt Based
    path("login/jwt", TokenObtainPairView.as_view(), name="jwt_login"),
    path("refresh/jwt", TokenRefreshView.as_view(), name="jwt_refresh"),
    # todo: add logout for jwt --blacklist token
]
