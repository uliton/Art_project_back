from django.conf import settings
from django.db import models


class Style(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Artist(models.Model):
    fullname = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=100)
    bio = models.TextField(max_length=100)
    mediums = models.ManyToManyField(to=Medium)
    phone = models.CharField(max_length=50)


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, related_name="artworks")
    image_url = models.URLField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="liked_artworks", blank=True)
    style = models.ForeignKey(to=Style, on_delete=models.CASCADE, related_name="artworks")
    medium = models.ForeignKey(to=Medium, on_delete=models.CASCADE, related_name="artworks")

    def __str__(self):
        return self.title




