from django.urls import include, path
from rest_framework import routers
from .views import ArtworkViewSet, CategoryViewSet, ArtistViewSet

router = routers.DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"categories", CategoryViewSet)
router.register("artists", ArtistViewSet, basename="artist")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "gallery"
