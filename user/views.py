from rest_framework import viewsets
from .serializers import UserSerializer, ArtistSerializer
from django.contrib.auth import get_user_model
from .models import Artist

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
