from rest_framework import viewsets
from .models import Artwork, Style, Medium
from .serializers import ArtworkSerializer, StyleSerializer, MediumSerializer


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer


class StyleViewSet(viewsets.ModelViewSet):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer


class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
