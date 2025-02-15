from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"list", views.PatientUsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserRegistrationApiView.as_view(), name="register"),
    path("login/", views.UserLoginApiView.as_view(), name="login"),
    path("logout/", views.UserLogoutApiView.as_view(), name="logout"),
    path("active/<uid64>/<token>/", views.Activate, name="active"),
]
