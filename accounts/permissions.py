from rest_framework import permissions
from .models import APIKey


class HasAPIKeyScope(permissions.BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.auth, APIKey):
            return True  # authenticated via JWT/session — no scope restriction applies

        required_scope = getattr(view, "required_scope", None)
        if required_scope is None:
            return True

        return request.auth.scope in (required_scope, APIKey.Scope.ALL)