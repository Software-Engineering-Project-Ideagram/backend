from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_exist_validator, letter_validator
from .models import Profile, ProfileLinks
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema
from ideagram.profiles.services import register, update_user_profile, follow_profile, add_social_media_to_profile, \
    change_password, send_password_change_verification_code
from ideagram.api.mixins import ApiAuthMixin, ActiveProfileMixin
from .selectors import get_user_profile, get_profile_social_media, get_profile_using_username, get_profile_followers, \
    get_profile_followings, get_general_user_profile

from ideagram.common.models import Address
from ideagram.common.utils import inline_model_serializer
from ..users.Exceptions import InvalidPassword
from ideagram.users.models import BaseUser

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

        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data
                        , status=status.HTTP_201_CREATED)


class UserProfileApi(ApiAuthMixin, APIView):
    class OutPutUserProfileSerializer(serializers.ModelSerializer):
        user = inline_model_serializer(
            serializer_model=BaseUser,
            serializer_name='output_user_profile_user',
            model_fields=['email']
        )()

        address = inline_model_serializer(
            serializer_name="user_profile_address_serializer",
            serializer_model=Address,
            model_fields=[
                'country', 'state', 'city', 'address', 'zip_code'
            ]
        )()

        class Meta:
            model = Profile
            fields = ('user', "username", "profile_image", "first_name", "last_name", "gender", "birth_date", "address", "bio"
                      , "follower_count", "following_count", "idea_count", "is_public", "is_active", "is_banned")

    class InputUpdateUserProfileSerializer(serializers.ModelSerializer):
        old_password = serializers.CharField(
            max_length=256,
            validators=[
                number_validator,
                letter_validator,
                special_char_exist_validator,
                MinLengthValidator(limit_value=8)
            ],
            required=False
        )
        new_password = serializers.CharField(
            max_length=256,
            validators=[
                number_validator,
                letter_validator,
                special_char_exist_validator,
                MinLengthValidator(limit_value=8)
            ],
            required=False
        )

        address = inline_model_serializer(
            serializer_name="user_profile_edit_address_serializer",
            serializer_model=Address,
            model_fields=[
                'country', 'state', 'city', 'address', 'zip_code'
            ]
        )(required=False)

        class Meta:
            model = Profile
            optional_fields = ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'bio', 'address',
                               'profile_image',
                               'is_public', 'old_password', 'new_password']
            required_fields = []
            fields = [*optional_fields, *required_fields]

            extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

        def validate(self, attrs):
            super().validate(attrs=attrs)
            if attrs.get('new_password', None) and attrs.get('old_password', None) is None:
                raise serializers.ValidationError("You must enter old password")

            return super().validate(attrs=attrs)

        def validate_username(self, username):
            profile = get_profile_using_username(username=username)
            if profile:
                raise serializers.ValidationError("This username is already exists")

            return username

    @extend_schema(responses=OutPutUserProfileSerializer, tags=['User'])
    def get(self, request):
        query = get_user_profile(user=request.user)
        return Response(self.OutPutUserProfileSerializer(instance=query).data)

    @extend_schema(request=InputUpdateUserProfileSerializer, responses=OutPutUserProfileSerializer, tags=['User'])
    def put(self, request):
        serializer = self.InputUpdateUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = get_user_profile(user=request.user)

        try:
            updated_profile = update_user_profile(profile=user_profile, data=serializer.validated_data)
        except InvalidPassword as ex:
            return Response("Invalid old password", status=status.HTTP_400_BAD_REQUEST)

        update_serializer = self.OutPutUserProfileSerializer(instance=updated_profile)
        return Response(data=update_serializer.data)



class GeneralProfileApi(APIView):
    class OutputGeneralUserProfileSerializer(serializers.ModelSerializer):
        user = inline_model_serializer(
            serializer_model=BaseUser,
            serializer_name='output_general_user_profile_user',
            model_fields=['email']
        )()

        address = inline_model_serializer(
            serializer_name="general_user_profile_address_serializer",
            serializer_model=Address,
            model_fields=[
                'country', 'state', 'city', 'address', 'zip_code'
            ]
        )()

        class Meta:
            model = Profile
            fields = ('user', "username", "profile_image", "first_name", "last_name", "gender", "birth_date", "address"
                      , "bio", "follower_count", "following_count", "idea_count")

    @extend_schema(responses=OutputGeneralUserProfileSerializer, tags=['User'])
    def get(self, request, username):
        query = get_general_user_profile(username=username)
        if not query:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        return Response(self.OutputGeneralUserProfileSerializer(instance=query).data)



class UserProfileFollowerListApi(APIView):
    class OutputFollowerProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['username', 'first_name', 'last_name', 'profile_image', 'follower_count', 'following_count',
                      'idea_count']

    @extend_schema(responses=OutputFollowerProfileSerializer(many=True), tags=['Follow'])
    def get(self, request, username):
        profile = get_profile_using_username(username=username)
        if not profile:
            return Response(data={'details': {"username": ["No profile found with this username"]}}
                            , status=status.HTTP_404_NOT_FOUND)
        followers = get_profile_followers(profile=profile)
        output_serializer = self.OutputFollowerProfileSerializer(instance=followers, many=True)
        return Response(data=output_serializer.data)



class UserProfileFollowingListApi(APIView):
    class OutputFollowingProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['username', 'first_name', 'last_name', 'profile_image', 'follower_count', 'following_count',
                      'idea_count']

    @extend_schema(responses=OutputFollowingProfileSerializer(many=True), tags=['Follow'])
    def get(self, request, username):
        profile = get_profile_using_username(username=username)
        if not profile:
            return Response(data={'details': {"username": ["No profile found with this username"]}}
                            , status=status.HTTP_404_NOT_FOUND)
        followers = get_profile_followings(profile=profile)
        output_serializer = self.OutputFollowingProfileSerializer(instance=followers, many=True)
        return Response(data=output_serializer.data)


class UserProfileSocialMediaApi(ApiAuthMixin, APIView):
    class InputSocialMediaSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProfileLinks
            fields = ['type', 'link']

    class OutputSocialMediaSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProfileLinks
            fields = ['uuid', 'type', 'link']

    @extend_schema(responses=OutputSocialMediaSerializer(many=True), tags=['Social Media'])
    def get(self, request):
        profile = get_user_profile(user=request.user)
        social_media = get_profile_social_media(profile=profile)
        serializer = self.OutputSocialMediaSerializer(instance=social_media, many=True)
        return Response(data=serializer.data)

    @extend_schema(request=InputSocialMediaSerializer, responses=OutputSocialMediaSerializer, tags=['Social Media'])
    def post(self, request):
        serializer = self.InputSocialMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = get_user_profile(user=request.user)
        link = add_social_media_to_profile(profile=profile, data=serializer.validated_data)
        if not link:
            return Response(
                data={'details': {'type': ["this social media type is already exists for this user"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        output_serializer = self.OutputSocialMediaSerializer(instance=link)
        return Response(data=output_serializer.data)


class UserProfileSocialMediaDetailApi(ApiAuthMixin, APIView):
    @extend_schema(tags=['Social Media'])
    def delete(self, request, social_media_uuid):
        profile = get_user_profile(user=request.user)
        try:
            social_media = ProfileLinks.objects.get(uuid=social_media_uuid, profile=profile)
        except:
            return Response(
                data={'details': {'social_media_uuid': ["No social media found with given uuid for this user"]}},
                status=status.HTTP_404_NOT_FOUND
            )

        social_media.delete()
        return Response(status=status.HTTP_200_OK)


class FollowProfileApi(ActiveProfileMixin, APIView):

    @extend_schema(tags=['Follow'])
    def post(self, request, following_username):
        try:
            follow_profile(user=request.user, following_username=following_username)
            return Response(status=status.HTTP_201_CREATED)
        except (Profile.DoesNotExist, ValueError):
            return Response(status=status.HTTP_404_NOT_FOUND)


class ForgetPasswordApi(APIView):
    class InputForgetPasswordSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=128, required=False)

    @extend_schema(request=InputForgetPasswordSerializer, tags=["Forget Password"])
    def post(self, request):
        serializer = self.InputForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            send_password_change_verification_code(**serializer.validated_data)
        except ValueError:
            return Response("invalid username", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)




class ChangePasswordApi(APIView):
    class InputChangePasswordSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=128, required=False)
        validation_code = serializers.CharField(max_length=6)
        new_password = serializers.CharField(
            max_length=256,
            validators=[
                number_validator,
                letter_validator,
                special_char_exist_validator,
                MinLengthValidator(limit_value=8)
            ]
        )

    @extend_schema(request=InputChangePasswordSerializer, tags=["Forget Password"])
    def post(self, request):
        serializer = self.InputChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_changed = change_password(**serializer.validated_data)
        if is_changed:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class DeleteProfileAPI(ApiAuthMixin, APIView):

    @extend_schema(tags=['User'])
    def delete(self, request):
        profile = get_user_profile(user=request.user)
        profile.is_active = False
        profile.save()
        return Response(statuse=status.HTTP_200_OK)
