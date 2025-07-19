from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.job_posting.models import JobPosting
from .serializers import JobPostingCreateSerializer, JobPostingUpdateSerializer, JobPostingListSerializer
from apps.api.permissions.permissions import FlexibleHRUserPermission


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.select_related("hr_company", "client_company").all()
    permission_classes = (FlexibleHRUserPermission, IsAuthenticated)

    def get_serializer_class(self):
        if self.action == "create":
            return JobPostingCreateSerializer
        if self.action in ["update", "partial_update"]:
            return JobPostingUpdateSerializer
        return JobPostingListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.can_manage_job_post(user=self.request.user)  # todo: ASK: need filter active job post ?
        return queryset

    def perform_create(self, serializer):
        serializer.save(hr_user=self.request.user)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        job_posting = self.get_object()
        job_posting.is_active = True
        job_posting.save(update_fields=["is_active"])
        return Response({"message": "İş ilanı aktif hale getirildi"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        job_posting = self.get_object()
        job_posting.is_active = False
        job_posting.save(update_fields=["is_active"])
        return Response({"message": "İş ilanı pasif hale getirildi"}, status=status.HTTP_200_OK)
