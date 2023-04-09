from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

BASE_USER = get_user_model()


def get_jwt_tokens(*, user: BASE_USER, password: str) -> dict:
    if user:
        user = authenticate(username=user.email, password=password)
    else:
        raise AuthenticationFailed("No active account found with given information.")

    if user:
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
    else:
        raise AuthenticationFailed("Invalid username/password.")
