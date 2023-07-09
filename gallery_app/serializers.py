from django.forms import CheckboxSelectMultiple
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Artwork, Category, Artist, ArtworkColor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ArtistSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ["fullname", "location", "bio", "phone", "image", "categories"]

    def get_categories(self, obj):
        category = self.context["request"].query_params.get("category")
        artworks = obj.artworks.all()

        if category:
            artworks = artworks.filter(categories__name__icontains=category)

        categories = artworks.values_list("categories__name", flat=True).distinct()
        return categories

    def validate_fullname(self, value):
        if Artist.objects.filter(fullname=value).exists():
            raise ValidationError("Artist with this fullname already exists.")
        return value


class ArtworkSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    likes_count = serializers.SerializerMethodField()
    color = serializers.MultipleChoiceField(
        choices=[(choice.value, choice.name) for choice in ArtworkColor],
        allow_blank=True,
        required=False,
    )

    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True
    )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        artist = validated_data.pop("artist")
        likes = validated_data.pop("likes", [])
        categories = validated_data.pop("categories", None)
        artwork = Artwork.objects.create(artist=artist, categories=categories, **validated_data)
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
            "year",
            "likes",
        ]
        read_only_fields = ["likes_count", "likes"]
