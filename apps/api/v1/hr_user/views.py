from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.permissions import CanHRUserManageJobPostingPermission
from apps.hr_user.models import HRUser
from .serializers import HRUserCreateSerializer, HRUserUpdateSerializer


class HRUserViewSet(viewsets.ModelViewSet):
    queryset = HRUser.objects.select_related("hr_company").prefetch_related("client_companies").all()
    permission_classes = (CanHRUserManageJobPostingPermission, IsAuthenticated)

    def get_serializer_class(self):
        if self.action == "create":
            return HRUserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return HRUserUpdateSerializer
        return HRUserUpdateSerializer

    def perform_update(self, serializer):
        super().perform_update(serializer)
