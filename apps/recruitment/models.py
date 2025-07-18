from django.db import models
from django.contrib.auth import get_user_model

from libs.abstract import TimeStampedModel


# 1. HRCompany: Human Resources company (İK şirketi)
class HRCompany(TimeStampedModel):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 2. ClientCompany: Client company (Müşteri şirketi)
class ClientCompany(TimeStampedModel):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 3. HRUser: HR user, linked to HRCompany and authorized ClientCompanies
#    (Not a custom user yet, just extends User with extra fields)
class HRUser(TimeStampedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    hr_company = models.ForeignKey(HRCompany, on_delete=models.CASCADE, related_name="hr_users")
    client_companies = models.ManyToManyField(ClientCompany, related_name="authorized_hr_users")

    def __str__(self):
        return f"{self.user.username} ({self.hr_company.name})"


# 4. JobPosting: Job post, linked to HRCompany and ClientCompany
class JobPosting(TimeStampedModel):
    hr_company = models.ForeignKey(HRCompany, on_delete=models.CASCADE, related_name="job_postings")
    client_company = models.ForeignKey(ClientCompany, on_delete=models.CASCADE, related_name="job_postings")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    closing_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.client_company.name})"


# 5. Candidate: Candidate profile
class Candidate(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 6. Education: Education info for Candidate
class Education(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.school} - {self.candidate.first_name} {self.candidate.last_name}"


# 7. WorkExperience: Work experience info for Candidate
class WorkExperience(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.candidate.first_name} {self.candidate.last_name}"


# 8. Status: Status for CandidateFlow (e.g. Positive, Negative, Completed)
class Status(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 9. CandidateFlow: Connects Candidate and JobPosting, tracks status and activities
class CandidateFlow(TimeStampedModel):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="candidate_flows")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_flows")
    hr_user = models.ForeignKey(
        HRUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows"
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="candidate_flows")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate} - {self.job_posting}"


# 10. Activity: Actions taken in CandidateFlow (e.g. phone call, email, test)
class Activity(TimeStampedModel):
    ACTIVITY_TYPE_CHOICES = [
        ("phone_call", "Phone Call"),
        ("email_sent", "Email Sent"),
        ("test_sent", "Test Sent"),
    ]
    candidate_flow = models.ForeignKey(CandidateFlow, on_delete=models.CASCADE, related_name="activities")
    hr_user = models.ForeignKey(HRUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.candidate_flow}"
