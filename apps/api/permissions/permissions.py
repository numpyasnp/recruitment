from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

from apps.api.permissions.base_permission import BasePermissionChecker

if TYPE_CHECKING:
    from apps.flow.models import CandidateFlow
    from apps.hr_user.models import HRUser
    from apps.job_posting.models import JobPosting


class JobPostingPermissionChecker(BasePermissionChecker):
    """Custom permission checker for JobPosting"""

    def can_manage(self, user: "HRUser", obj: "JobPosting"):
        return obj.is_manageable_by_hr_user


class CandidateFlowPermissionChecker(BasePermissionChecker):
    """Custom permission checker for WorkExperience"""

    def can_manage(self, user: "HRUser", obj: "CandidateFlow"):
        return (
            user.hr_company == obj.job_posting.hr_company
            and obj.job_posting.client_company in user.client_companies.all()
        )


class DefaultPermissionChecker(BasePermissionChecker):
    """Default permission checker for unknown models"""

    def can_manage(self, user, obj):
        if hasattr(obj, "is_manageable_by_hr_user"):
            return obj.is_manageable_by_hr_user
        return False


class FlexibleHRUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and hasattr(request.user, "hr_company")

    def has_object_permission(self, request, view, obj):
        from apps.api.permissions.permission_factory import PermissionFactory

        return PermissionFactory.can_manage(request.user, obj)
