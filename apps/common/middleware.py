# apps/common/middleware.py

from django.contrib.auth.middleware import AuthenticationMiddleware as DjangoAuthMiddleware
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from .current_user import set_current_user, clear_current_user

# Keep the same import path your settings referenced:
# 'apps.common.middleware.AuthenticationMiddleware'
AuthenticationMiddleware = DjangoAuthMiddleware

# Your existing middleware (slightly hardened)
class CurrentUserMiddleware(MiddlewareMixin):
    """
    Sets the current user into a thread-local / context at request start and clears it after the response.
    Assumes Django's AuthenticationMiddleware (or equivalent) runs before this middleware so request.user is set.
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # Defensive: some middleware chains might call this before auth middleware,
        # so make sure we pass a sensible value (AnonymousUser if not authenticated).
        user = getattr(request, "user", None)
        set_current_user(user)

        try:
            response = self.get_response(request) if self.get_response else HttpResponse()
            return response
        finally:
            clear_current_user()


__all__ = [
    "AuthenticationMiddleware",
    "CurrentUserMiddleware",
]
