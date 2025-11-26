from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from apps.courses.models import Course


class IsOwner(BasePermission):
    """Allow access only to the owner of the object."""

    message = "You do not have permission to modify this course."

    def has_object_permission(self, request: Request, view: ViewSet, obj: Course) -> bool:
        return obj.owner_id == getattr(request.user, 'id', None)
