from django.urls import path
from .apis import UserProfileApi, RegisterApi


urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
]