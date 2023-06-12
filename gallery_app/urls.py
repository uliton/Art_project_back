from django.urls import include, path
from rest_framework import routers
from .views import ArtworkViewSet, StyleViewSet, MediumViewSet, ArtistViewSet

router = routers.DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"styles", StyleViewSet)
router.register(r"medium", MediumViewSet)
router.register('artists', ArtistViewSet, basename='artist')

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "gallery"
