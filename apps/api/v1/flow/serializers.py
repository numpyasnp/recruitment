from rest_framework import serializers
from apps.flow.models import CandidateFlow


class CandidateFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateFlow
        fields = [
            "id",
            "job_posting",
            "candidate",
            "hr_user",
            "status",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["id", "date_created", "date_updated", "hr_user"]

    def validate(self, attrs):
        user = self.context["request"].user
        job_posting = attrs.get("job_posting")
        if job_posting and hasattr(user, "client_companies"):
            if job_posting.client_company not in user.client_companies.all():
                raise serializers.ValidationError(
                    "You are not authorized to create a candidate flow for this job posting's client company."
                )
        return attrs
