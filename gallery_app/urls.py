from django.urls import include, path
from rest_framework import routers

from .views import ArtworkViewSet, CategoryViewSet, ArtistViewSet, LikeCreateView, LikedArtworksView

router = routers.DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"categories", CategoryViewSet)
router.register("artists", ArtistViewSet, basename="artist")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "artworks/<int:pk>/like/create/",
        LikeCreateView.as_view(),
        name="like-create"
    ),
    path(
        "liked/",
        LikedArtworksView.as_view(),
        name="liked-artworks"
    ),
]

app_name = "gallery"
