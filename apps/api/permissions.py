from rest_framework.permissions import BasePermission


class CanHRUserManageJobPostingPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_manageable_by_hr_user
