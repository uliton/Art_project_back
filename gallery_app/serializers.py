from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Artwork, Category, Artist, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ArtworkSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )
    likes = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True
    )

    @staticmethod
    def get_color(obj):
        return obj.color.split(',') if obj.color else []

    @staticmethod
    def get_likes(obj):
        return obj.liked_by.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['color'] = list(representation['color'])
        return representation

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
            "color",
            "categories",
            "year",
            "likes",
        ]
        read_only_fields = ["likes"]


class ArtistSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    artworks = ArtworkSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ["id", "fullname", "location", "bio", "phone", "image", "categories", "artworks"]

    def get_categories(self, obj):
        category = self.context["request"].query_params.get("category")
        artworks = obj.artworks.all()

        if category:
            artworks = artworks.filter(categories__name__icontains=category)

        categories = artworks.values_list("categories__name", flat=True).distinct()
        return categories

    @staticmethod
    def validate_fullname(value):
        if Artist.objects.filter(fullname=value).exists():
            raise ValidationError("Artist with this fullname already exists.")
        return value


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    artwork = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ["user", "artwork"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        artwork = self.context.get("artwork")

        if Like.objects.filter(user=user, artwork=artwork).exists():
            raise serializers.ValidationError("You have already liked this artwork.")

        return attrs
