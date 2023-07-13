from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from pagination import ArtGalleryListPagination
from .models import Artwork, Category, Artist, Like
from .serializers import (
    ArtworkSerializer,
    CategorySerializer,
    ArtistSerializer,
    LikeSerializer, ArtworkCreateSerializer,
)


class BaseArtViewSet(viewsets.ModelViewSet):
    pagination_class = ArtGalleryListPagination
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return super().get_permissions()


class ArtworkViewSet(BaseArtViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        artwork = self.get_object()
        user = request.user
        liked_by_user = artwork.likes.filter(id=user.id).exists()

        if liked_by_user:
            artwork.likes.remove(user)
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        else:
            artwork.likes.add(user)
            return Response({'message': 'Like added'}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        color = self.request.query_params.get("color")
        category = self.request.query_params.get("category")
        title = self.request.query_params.get("title")
        artist = self.request.query_params.get("artist")

        if color and category:
            queryset = queryset.filter(
                Q(color__icontains=color) & Q(categories__name__icontains=category)
            )
        elif color:
            queryset = queryset.filter(color__icontains=color)
        elif category:
            queryset = queryset.filter(categories__name__icontains=category)

        elif title:
            queryset = queryset.filter(title__icontains=title)

        elif category and artist:
            queryset = queryset.filter(
                Q(categories__name__icontains=category)
                & Q(artist__fullname__icontains=artist)
            )
        elif artist:
            queryset = queryset.filter(artist__fullname__icontains=artist)
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return ArtworkCreateSerializer
        return ArtworkSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        location = self.request.query_params.get("location")

        if category:
            queryset = queryset.filter(artworks__categories__name__icontains=category).distinct()

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset


class LikeCreateView(generics.CreateAPIView):
    """Endpoint for create like"""

    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        artwork = self.get_artwork()
        user = self.request.user
        serializer.save(user=user, artwork=artwork)

    def get_artwork(self):
        artwork_id = self.kwargs["pk"]
        artwork = get_object_or_404(Artwork, pk=artwork_id)
        return artwork

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["artwork"] = self.get_artwork()
        return context


class LikedArtworksView(generics.ListAPIView):
    serializer_class = ArtworkSerializer
    pagination_class = ArtGalleryListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        liked_artwork_ids = Like.objects.filter(user=user).values_list("artwork", flat=True)
        return Artwork.objects.filter(id__in=liked_artwork_ids)
