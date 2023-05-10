from django.urls import path

from ideagram.reports.apis import ProfileReportAPI, IdeaReportAPI

urlpatterns = [
    path('profile/', ProfileReportAPI.as_view(), name="ProfileReport"),
    path('idea/', IdeaReportAPI.as_view(), name="IdeaReport")
]
