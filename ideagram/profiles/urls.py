from django.urls import path
from .apis import UserProfileApi, RegisterApi, UserProfileSocialMediaApi

urlpatterns = [
    path('user/register/', RegisterApi.as_view(), name="register"),
    path('user/profile/', UserProfileApi.as_view(), name="user-profile"),
    path('user/social-media/', UserProfileSocialMediaApi.as_view(), name="user-social-media"),
]
