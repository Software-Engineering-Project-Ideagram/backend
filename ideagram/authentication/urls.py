from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from .apis import LoginView, TokenRefreshView

urlpatterns = [
    path('jwt/', include(([
        path('login/', LoginView.as_view(), name="login"),
        path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    ])), name="jwt"),
]
