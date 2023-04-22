from django.urls import path

from ideagram.ideas.apis import ClassificationAPI, IdeaCreateAPI, IdeaDetailView

urlpatterns = [
    path('classification/list', ClassificationAPI.as_view(), name="classification-list"),
    path('idea/create', IdeaCreateAPI.as_view(), name="idea-create"),
    path('idea/detail/<str:idea_uuid>', IdeaDetailView.as_view(), name='idea-detail'),
]
