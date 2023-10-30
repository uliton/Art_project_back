from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Artwork, Category, Artist, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ArtistFullnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'fullname')


class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistFullnameSerializer()
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


class ArtworkCreateSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )
    color = serializers.MultipleChoiceField(choices=Artwork.COLOR_CHOICES)
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
        color_codes = representation['color']
        color_names = [dict(Artwork.COLOR_CHOICES).get(code) for code in color_codes]
        representation['color'] = [color_names] if color_names else []
        return representation

    def create(self, validated_data):
        artist = validated_data.pop("artist")
        categories = validated_data.pop("categories", None)
        colors = validated_data.pop("color", None)
        artwork = Artwork.objects.create(artist=artist, categories=categories, color=colors, **validated_data)
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
        ]


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