from django.conf import settings
from rest_framework.permissions import BasePermission

from .models import Token


class HasValidToken(BasePermission):
    """
    Requires a valid token in the Authorization header.
    Format: Authorization: Bearer <token_value>
    """

    def has_permission(self, request, view):
        if not getattr(settings, "AUTH_REQUIRED", True):
            return True

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            self.message = "Authorization header must use Bearer scheme"
            return False

        token_value = auth_header[7:]
        if not token_value:
            self.message = "Token value is empty"
            return False

        try:
            token = Token.objects.get(value=token_value)
        except Token.DoesNotExist:
            self.message = "Invalid token"
            return False

        if not token.is_valid:
            if token.status != "active":
                self.message = "Token is inactive"
            else:
                self.message = "Token has expired"
            return False

        return True
