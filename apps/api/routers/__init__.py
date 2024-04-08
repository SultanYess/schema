from django.urls import path, include

urlpatterns = [
    path("main/", include("apps.api.routers.main")),
    # path('auth/', include('apps.api.routers.auth'))
]
