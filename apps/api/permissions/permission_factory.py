from apps.api.permissions.base_permission import BasePermissionChecker
from apps.api.permissions.permissions import (
    JobPostingPermissionChecker,
    DefaultPermissionChecker,
    CandidateFlowPermissionChecker,
)
from apps.flow.models import CandidateFlow
from apps.job_posting.models import JobPosting


class PermissionFactory:
    @staticmethod
    def get_permission_checker(obj) -> BasePermissionChecker:
        if isinstance(obj, JobPosting):
            return JobPostingPermissionChecker()
        elif isinstance(obj, CandidateFlow):
            return CandidateFlowPermissionChecker()
        else:
            return DefaultPermissionChecker()

    @staticmethod
    def can_manage(user, obj) -> bool:
        """Check if the user can manage the object."""
        checker = PermissionFactory.get_permission_checker(obj)
        return checker.can_manage(user, obj)
