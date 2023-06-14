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

        if color and category:
            queryset = queryset.filter(
                Q(color__iexact=color) & Q(categories__name__iexact=category)
            )
        elif color:
            queryset = queryset.filter(color__iexact=color)
        elif category:
            queryset = queryset.filter(categories__name__iexact=category)

        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
