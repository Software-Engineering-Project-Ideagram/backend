from rest_framework.permissions import BasePermission

from ideagram.profiles.models import Profile


class IsProfileActive(BasePermission):
    """
    Allows access only to active profile.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.is_user_active):
            return False

        profile = Profile.objects.filter(user=request.user)

        if profile.exists() and profile.first().is_profile_active:
            return True
        else:
            return False
