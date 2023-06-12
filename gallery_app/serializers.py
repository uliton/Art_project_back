from rest_framework import serializers
from .models import Artwork, Style, Medium, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["fullname", 'location', "bio", "phone"]


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


