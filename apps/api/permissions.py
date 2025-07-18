from rest_framework.permissions import BasePermission


class CanHRUserManageJobPostingPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        hr_user = request.user

        if hr_user.hr_companpy == obj.hr_company and hr_user.client_company == obj.client_company:
            return True
        return False
