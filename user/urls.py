from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet, ArtistViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('artists', ArtistViewSet, basename='artist')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "user"