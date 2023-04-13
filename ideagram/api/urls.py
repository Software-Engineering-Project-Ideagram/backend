from django.urls import path, include

urlpatterns = [
    path('auth/', include('ideagram.authentication.urls')),
    path('user/', include("ideagram.profiles.urls")),
    path('idea/', include("ideagram.ideas.urls")),
    ]
