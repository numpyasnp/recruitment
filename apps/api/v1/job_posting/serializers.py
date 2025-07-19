from rest_framework import serializers
from apps.job_posting.models import JobPosting
from apps.job_posting.errors.errors import PermissionDenied


class JobPostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            "id",
            "hr_user",
            "hr_company",
            "client_company",
            "title",
            "description",
            "closing_date",
            "is_active",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]

    def validate(self, attrs):
        user = self.context["request"].user
        if attrs.get("hr_company") != user.hr_company or attrs.get("client_company") not in user.client_companies.all():
            raise PermissionDenied()
        return attrs


class JobPostingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            "id",
            "hr_company",
            "hr_user",
            "client_company",
            "title",
            "description",
            "closing_date",
            "is_active",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]


class JobPostingListSerializer(serializers.ModelSerializer):
    hr_company_name = serializers.CharField(source="hr_company.name", read_only=True)
    client_company_name = serializers.CharField(source="client_company.name", read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "hr_company",
            "hr_user",
            "hr_company_name",
            "client_company",
            "client_company_name",
            "title",
            "description",
            "closing_date",
            "is_active",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]
