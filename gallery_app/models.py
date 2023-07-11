from django.conf import settings
from django.db import models
from enum import Enum


class ArtworkColor(Enum):
    BEIGE = "Beige"
    BLACK = "Black"
    BLUE = "Blue"
    BROWN = "Brown"
    GOLD = "Gold"
    GREEN = "Green"
    GREY = "Grey"
    ORANGE = "Orange"
    PINK = "Pink"
    PURPLE = "Purple"
    RED = "Red"
    SILVER = "Silver"
    WHITE = "White"
    YELLOW = "Yellow"
    MULTI = "Multi"
    BLACK_AND_WHITE = "Black & White"


class ArtworkCategory(Enum):
    PAINTING = "Painting"
    PHOTOGRAPHY = "Photography"
    SCULPTURE = "Sculpture"
    PRINTS = "Prints"
    WORK_ON_PAPER = "Work on paper"
    DESIGN = "Design"
    GRAPHIC_DESIGN = "Graphic design"
    COLLAGES = "Collages"
    ILLUSTRATION = "Illustration"


class Category(models.Model):
    CATEGORY_CHOICES = [(tag.value, tag.value) for tag in ArtworkCategory]

    name = models.CharField(choices=CATEGORY_CHOICES, max_length=255, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    fullname = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=100)
    bio = models.TextField(max_length=100)
    categories = models.ManyToManyField(to=Category)
    phone = models.CharField(max_length=50)
    image = models.ImageField()


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        to=Artist, on_delete=models.CASCADE, related_name="artworks"
    )
    image_url = models.URLField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    likes = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="liked_artworks", blank=True
    )
    categories = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="artworks"
    )

    COLOR_CHOICES = [(tag.name, tag.value) for tag in ArtworkColor]

    color = models.CharField(choices=COLOR_CHOICES, max_length=100)
    year = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return self.title
