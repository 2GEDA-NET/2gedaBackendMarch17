from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"user-profiles", UserProfileViewSet)
router.register(r"business-categories", BusinessCategoryViewSet)
router.register(r"password-change", PasswordChangeViewSet, basename="password-change")

urlpatterns = [
    path("api/", include(router.urls)),
    #     Authentication urls
    path("register/", create_user, name="user_register"),
    path("login/", login_view, name="api_token"),
    path("logout/", logout_view, name="api_token"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("resend-otp/", resend_otp, name="resend-otp"),
    #     path('password-change/', PasswordChangeViewSet.as_view, name='change_password'),
    path("", UserAPIView.as_view(), name="user_detail"),
]

urlpatterns += router.urls
