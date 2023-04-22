from django.urls import path

from ideagram.ideas.apis import ClassificationAPI, IdeaCreateAPI

urlpatterns = [
    path('classification/list', ClassificationAPI.as_view(), name="classification-list"),
    path('idea/create', IdeaCreateAPI.as_view(), name="idea-create"),
]
