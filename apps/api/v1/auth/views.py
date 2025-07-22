from django.contrib.auth import authenticate, login
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from apps.api.v1.auth.serializers import LoginSerializer
from apps.hr_user.errors.errors import AccountDoesNotExist

logger = logging.getLogger(__name__)


class HRSessionLoginView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email").lower()
        password = serializer.validated_data.get("password")

        user = authenticate(request, email=email, password=password)
        if not user:
            raise AccountDoesNotExist()

        login(request, user)
        self.update_last_login(user)

        logger.info(
            "Session login successful",
            extra={
                "ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "email": email,
                "user_id": user.id,
            },
        )

        return Response({"message": _("Login successful")}, status=200)

    def update_last_login(self, user):
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])


class HRSessionLogoutView(APIView):
    def post(self, request):
        logout(request)
        logger.info(
            "Session logout successful",
            extra={
                "ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "user_id": request.user.id,
            },
        )
        return Response({"message": _("Logout successful")}, status=200)
