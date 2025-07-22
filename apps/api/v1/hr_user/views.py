from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.hr_user.models import HRUser
from .serializers import HRUserCreateSerializer, HRUserUpdateSerializer
from apps.api.v1.utils import log_api_info


class HRUserViewSet(viewsets.ModelViewSet):
    queryset = HRUser.objects.select_related("hr_company").prefetch_related("client_companies").all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return HRUserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return HRUserUpdateSerializer
        return HRUserUpdateSerializer

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def create(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "create")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "update")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "partial_update")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "destroy")
        return super().destroy(request, *args, **kwargs)
