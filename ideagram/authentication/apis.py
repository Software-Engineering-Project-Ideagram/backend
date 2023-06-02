from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase

from ideagram.authentication.selectors import get_user_from_username
from ideagram.authentication.services import get_jwt_tokens
from ideagram.profiles.models import Profile
from ideagram.profiles.selectors import get_user_profile


class LoginView(APIView):
    class InputLoginSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=256)
        password = serializers.CharField(max_length=256)

    class OutputLoginSerializer(serializers.Serializer):
        refresh = serializers.CharField()
        access = serializers.CharField()

    @extend_schema(request=InputLoginSerializer, responses=OutputLoginSerializer, tags=['Auth'])
    def post(self, request):
        serializer = self.InputLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_from_username(username=serializer.validated_data['username'])
        data = get_jwt_tokens(user=user, password=serializer.validated_data['password'])
        output_serializer = self.OutputLoginSerializer(data=data)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER

    @extend_schema(tags=['Auth'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
