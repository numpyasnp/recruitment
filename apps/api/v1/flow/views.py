from rest_framework import viewsets

from apps.api.permissions.permissions import FlexibleHRUserPermission
from apps.flow.models import CandidateFlow
from .serializers import CandidateFlowSerializer


class CandidateFlowViewSet(viewsets.ModelViewSet):
    queryset = CandidateFlow.objects.select_related("job_posting", "candidate", "hr_user", "status").all()
    serializer_class = CandidateFlowSerializer
    permission_classes = [FlexibleHRUserPermission]

    def perform_create(self, serializer):
        serializer.save(hr_user=self.request.user)
