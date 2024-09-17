from rest_framework import permissions

class AuthorAllReadOnlyExceptStaff(permissions.BasePermission):
    write_methods = ("POST", "PUT", "PATCH")


    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method in self.write_methods:
            return True

        return False