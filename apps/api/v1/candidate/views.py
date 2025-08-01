from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.api.permissions.permissions import FlexibleHRUserPermission
from apps.candidate.models import Candidate, Education, WorkExperience
from .serializers import (
    CandidateCreateSerializer,
    CandidateUpdateSerializer,
    CandidateListSerializer,
    CandidateDetailSerializer,
    EducationSerializer,
    WorkExperienceSerializer,
)
from apps.api.v1.utils import log_api_info


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.prefetch_related("educations", "work_experiences").all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CandidateCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CandidateUpdateSerializer
        if self.action == "retrieve":
            return CandidateDetailSerializer
        return CandidateListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtreleme seçenekleri
        first_name = self.request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)
        email = self.request.query_params.get("email", None)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

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

    @action(detail=True, methods=["get", "post"])
    def educations(self, request, pk=None):
        log_api_info(request, self.__class__.__name__, "educations")
        """Adayın eğitim bilgilerini yönet"""
        candidate = self.get_object()
        if request.method == "GET":
            educations = candidate.educations.all()
            serializer = EducationSerializer(educations, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = EducationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(candidate=candidate)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return None

    @action(detail=True, methods=["get", "post"])
    def work_experiences(self, request, pk=None):
        log_api_info(request, self.__class__.__name__, "work_experiences")
        """Adayın iş deneyimi bilgilerini yönet"""
        candidate = self.get_object()

        if request.method == "GET":
            work_experiences = candidate.work_experiences.all()
            serializer = WorkExperienceSerializer(work_experiences, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = WorkExperienceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(candidate=candidate)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return None


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (FlexibleHRUserPermission,)

    def get_queryset(self):
        queryset = super().get_queryset()
        candidate_id = self.request.query_params.get("candidate", None)

        if candidate_id:
            queryset = queryset.filter(candidate_id=candidate_id)

        return queryset

    def list(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "retrieve")
        return super().retrieve(request, *args, **kwargs)

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


class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = (FlexibleHRUserPermission,)

    def get_queryset(self):
        queryset = super().get_queryset()
        candidate_id = self.request.query_params.get("candidate", None)

        if candidate_id:
            queryset = queryset.filter(candidate_id=candidate_id)

        return queryset

    def list(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_api_info(request, self.__class__.__name__, "retrieve")
        return super().retrieve(request, *args, **kwargs)

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
