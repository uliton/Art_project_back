from rest_framework import viewsets
from .models import Artwork, Category, Artist
from django.db.models import Q
from .serializers import (
    ArtworkSerializer,
    CategorySerializer,
    ArtistSerializer,
)


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

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
