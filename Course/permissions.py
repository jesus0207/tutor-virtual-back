from rest_framework import permissions


class IsCoursePermission(permissions.BasePermission):
    """
    Permission class to check if the requesting user is the owner of an object.
    """
    def has_object_permission(self, request, view, obj):
        """
        Method to determine if the requesting user has permission to access the object.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view instance associated with the request.
            obj: The object being accessed.

        Returns:
            bool: True if the requesting user is the owner of the object, False otherwise.
        """
        return obj.instructor.id == request.user.id