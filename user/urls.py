# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# from user.views import UserViewSet
# router = DefaultRouter()
# router.register('users', UserViewSet, basename='user')
#
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
#
# app_name = "user"

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
]