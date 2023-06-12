from rest_framework import serializers

from user.serializers import ArtistSerializer
from .models import Artwork, Style, Medium


class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Artwork
        fields = ['id', 'title', 'artist', 'image_url', 'description', 'price', 'likes', 'likes_count', 'style']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['id', 'name']


class MediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium
        fields = ['id', 'name']
