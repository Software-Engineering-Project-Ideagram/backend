from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_exist_validator, letter_validator
from .models import Profile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema
from ideagram.profiles.services import register
from ideagram.api.mixins import ApiAuthMixin
from ideagram.common.models import Address
from ideagram.common.utils import inline_model_serializer

BASE_USER = get_user_model()
class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        username = serializers.CharField(max_length=128)
        password = serializers.CharField(
            max_length=256,
            validators=[
                number_validator,
                letter_validator,
                special_char_exist_validator,
                MinLengthValidator(limit_value=8)
            ]
        )

        def validate_email(self, email):
            if BASE_USER.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email



    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BASE_USER
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer, tags=['User'])
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
            username=serializer.validated_data.get("username"),
        )

        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)
