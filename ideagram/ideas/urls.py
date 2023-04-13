from django.urls import path

from ideagram.ideas.apis import ClassificationAPI

urlpatterns = [
    path('classification/list', ClassificationAPI.as_view(), name="classification-list"),
]
