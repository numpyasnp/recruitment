from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils.translation import gettext_lazy as _


from apps.job_posting.models import JobPosting
from .serializers import JobPostingCreateSerializer, JobPostingUpdateSerializer, JobPostingListSerializer
from apps.api.permissions.permissions import FlexibleHRUserPermission
from apps.api.v1.paginators import JobPostingPaginator
from apps.api.v1.utils import log_api_info


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.select_related("hr_company", "client_company").all()
    permission_classes = (FlexibleHRUserPermission,)
    pagination_class = JobPostingPaginator

    def get_serializer_class(self):
        if self.action == "create":
            return JobPostingCreateSerializer
        if self.action in ["update", "partial_update"]:
            return JobPostingUpdateSerializer
        return JobPostingListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.can_manage_job_post_by(user=self.request.user)  # todo: ASK: need filter active job post ?
        return queryset

    def perform_create(self, serializer):
        serializer.save(hr_user=self.request.user)

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

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        log_api_info(request, self.__class__.__name__, "activate")
        job_posting = self.get_object()
        job_posting.is_active = True
        job_posting.save(update_fields=["is_active"])
        return Response({"message": _("The job posting has been activated.")}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        log_api_info(request, self.__class__.__name__, "deactivate")
        job_posting = self.get_object()
        job_posting.is_active = False
        job_posting.save(update_fields=["is_active"])
        return Response({"message": _("The job posting has been deactivated.")}, status=status.HTTP_200_OK)
