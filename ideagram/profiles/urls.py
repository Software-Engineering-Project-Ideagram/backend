from django.urls import path
from .apis import UserProfileApi, RegisterApi, UserProfileSocialMediaApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('profile/', UserProfileApi.as_view(), name="user-profile"),
    path('social-media/', UserProfileSocialMediaApi.as_view(), name="user-social-media"),
]
