from django.urls import path
from .apis import UserProfileApi, RegisterApi, UserProfileSocialMediaApi, FollowProfileApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('profile/', UserProfileApi.as_view(), name="user-profile"),
    path('social-media/', UserProfileSocialMediaApi.as_view(), name="user-social-media"),
    path('follow-profile/<str:following_username>', FollowProfileApi.as_view(), name="user-follow")
]
