from django.urls import path

from ideagram.reports.apis import ProfileReportAPI

urlpatterns = [
    path('profile/', ProfileReportAPI.as_view(), name="ProfileReport")
]
