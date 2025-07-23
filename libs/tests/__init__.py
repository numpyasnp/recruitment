import random
import string

from model_bakery import baker

from apps.hr_user.models import HRUser
from apps.candidate.models import Candidate
from apps.flow.models import CandidateFlow
from apps.job_posting.models import JobPosting


def create_hr_user(name: str = "", email: str = "", password="test123", **kwargs) -> HRUser:
    email = email or generate_random_email()
    name = name or "jhon doe"
    user = baker.make(HRUser, name=name, email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user


def create_candidate_flow(**kwargs):
    hr_user = create_hr_user(is_active=True)
    candidate = baker.make(Candidate, email=generate_random_email(), hr_user=hr_user)
    job_post = baker.make(JobPosting, hr_user=hr_user)
    candidate_flow = baker.make(CandidateFlow, candidate=candidate, hr_user=hr_user, job_posting=job_post, **kwargs)
    return candidate_flow


def generate_random_email(domain: str = "example.com") -> str:
    """Rastgele e-mail adresi üretir."""
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@{domain}"
