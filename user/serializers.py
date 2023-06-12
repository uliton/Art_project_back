from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Artist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'fullname', "password", 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ["fullname",'location', "bio", "phone"]
