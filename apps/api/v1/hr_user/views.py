from rest_framework import viewsets
from apps.hr_user.models import HRUser
from .serializers import HRUserCreateSerializer, HRUserUpdateSerializer


class HRUserViewSet(viewsets.ModelViewSet):
    queryset = HRUser.objects.select_related("hr_company").prefetch_related("client_companies").all()

    def get_serializer_class(self):
        if self.action == "create":
            return HRUserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return HRUserUpdateSerializer
        return HRUserUpdateSerializer
