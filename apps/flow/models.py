from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from apps.hr_user.models import HRUser
from libs.abstract.models import TimeStampedModel


class Status(TimeStampedModel):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        db_table = "status"


class Activity(TimeStampedModel):
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        db_table = "activity"


class CandidateFlowQuerySet(QuerySet):

    def managed_by_user(self, user: HRUser):
        return self.filter(job_posting__hr_user=user)


class CandidateFlow(TimeStampedModel):
    job_posting = models.ForeignKey("job_posting.JobPosting", on_delete=models.CASCADE, related_name="candidate_flows")
    candidate = models.ForeignKey("candidate.Candidate", on_delete=models.CASCADE, related_name="candidate_flows")
    hr_user = models.ForeignKey(
        "hr_user.HRUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows"
    )
    status = models.ForeignKey(
        "Status", on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows"
    )
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name="candidate_flows")

    objects = CandidateFlowQuerySet.as_manager()

    def __str__(self):
        return f"{self.candidate} - {self.job_posting}"

    class Meta:
        unique_together = ("job_posting", "candidate")
        verbose_name = "Candidate Flow"
        verbose_name_plural = "Candidate Flows"
        db_table = "candidate_flow"


class CandidateActivityLogQuerySet(QuerySet):
    def from_year_start(self):
        now = timezone.now()
        year_start = timezone.datetime(now.year, 1, 1, tzinfo=now.tzinfo)
        return self.filter(date_created__gte=year_start)


class CandidateFlowLog(TimeStampedModel):
    candidate_flow = models.ForeignKey("CandidateFlow", on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[("create", "Create"), ("update", "Update"), ("delete", "Delete")])
    performed_by = models.ForeignKey("hr_user.HRUser", null=True, on_delete=models.SET_NULL)
    changes = models.JSONField(null=True, blank=True)

    objects = CandidateActivityLogQuerySet.as_manager()

    class Meta:
        verbose_name = "Candidate Flow Log"
        verbose_name_plural = "Candidate Flow Logs"
        db_table = "candidate_flow_log"
