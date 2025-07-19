import abc


class BasePermissionChecker(abc.ABC):
    """Base permission checker class"""

    @abc.abstractmethod
    def can_manage(self, user, obj):
        raise NotImplementedError
