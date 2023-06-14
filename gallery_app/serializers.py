from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Artwork, Category, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["fullname", "location", "bio", "phone"]

    def validate_fullname(self, value):
        if Artist.objects.filter(fullname=value).exists():
            raise ValidationError("Artist with this fullname already exists.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    likes_count = serializers.SerializerMethodField()
    categories = CategorySerializer(read_only=False)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        artist_data = validated_data.pop("artist")
        artist = Artist.objects.create(**artist_data)
        likes = validated_data.pop("likes", [])
        artwork = Artwork.objects.create(artist=artist, **validated_data)
        artwork.likes.set(likes)
        return artwork

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "artist",
            "image_url",
            "description",
            "price",
            "likes_count",
            "color",
            "categories",
            "likes",
        ]
        read_only_fields = ["likes_count", "likes"]
