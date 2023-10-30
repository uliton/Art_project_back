from django.contrib import admin
from gallery_app.models import Artist
from gallery_app.models import Artwork
from gallery_app.models import Category

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("fullname", "location", "phone")
    search_fields = ("fullname", "location", "phone")

admin.site.register(Artwork)

admin.site.register(Category)
