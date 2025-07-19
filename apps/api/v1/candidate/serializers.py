from rest_framework import serializers
from apps.candidate.models import Candidate, Education, WorkExperience


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "school",
            "department",
            "start_date",
            "end_date",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            "id",
            "company",
            "position",
            "tech_stack",
            "start_date",
            "end_date",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class CandidateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class CandidateListSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "educations",
            "work_experiences",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class CandidateDetailSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "educations",
            "work_experiences",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]
