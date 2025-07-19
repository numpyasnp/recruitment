from django.db import models

from libs.abstract.models import TimeStampedModel


class Status(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        db_table = "status"


class CandidateFlow(TimeStampedModel):
    job_posting = models.ForeignKey("job_posting.JobPosting", on_delete=models.CASCADE, related_name="candidate_flows")
    candidate = models.ForeignKey("candidate.Candidate", on_delete=models.CASCADE, related_name="candidate_flows")
    hr_user = models.ForeignKey(
        "hr_user.HRUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows"
    )
    status = models.ForeignKey(
        "Status", on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows"
    )

    def __str__(self):
        return f"{self.candidate} - {self.job_posting}"

    class Meta:
        unique_together = ("job_posting", "candidate")
        verbose_name = "Candidate Flow"
        verbose_name_plural = "Candidate Flows"
        db_table = "candidate_flow"


class Activity(TimeStampedModel):
    name = models.CharField(max_length=255)
    candidate_flow = models.ForeignKey("CandidateFlow", on_delete=models.CASCADE, related_name="activities")
    hr_user = models.ForeignKey(
        "hr_user.HRUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="activities"
    )
    status = models.ForeignKey("Status", on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.candidate_flow}"

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        db_table = "activity"


class CandidateActivityLog(TimeStampedModel):
    candidate_flow = models.ForeignKey(CandidateFlow, on_delete=models.CASCADE, related_name="candidate_activities_log")
    activity_type = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name="candidate_activities_log")
    status_type = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="candidate_activities_log")
    created_by = models.ForeignKey(
        "hr_user.HRUser", on_delete=models.SET_NULL, null=True, related_name="candidate_activities_log"
    )
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Candidate Activity Log"
        verbose_name_plural = "Candidate Activity Logs"
        db_table = "candidate_activity_log"
