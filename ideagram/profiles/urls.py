from django.urls import path
from .apis import UserProfileApi, RegisterApi, UserProfileSocialMediaApi, FollowProfileApi, \
    UserProfileSocialMediaDetailApi, UserProfileFollowerListApi, UserProfileFollowingListApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('profile/', UserProfileApi.as_view(), name="user-profile"),
    path('profile/followers/<str:username>', UserProfileFollowerListApi.as_view(), name="profile-followers"),
    path('profile/followings/<str:username>', UserProfileFollowingListApi.as_view(), name="profile-followings"),
    path('social-media/', UserProfileSocialMediaApi.as_view(), name="user-social-media"),
    path('social-media/<str:social_media_uuid>',
         UserProfileSocialMediaDetailApi.as_view(),
         name="user-social-media-detail"
         ),
    path('follow-profile/<str:following_username>', FollowProfileApi.as_view(), name="user-follow")
]
