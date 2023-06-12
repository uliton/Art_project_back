from django.contrib import admin
from gallery_app.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("fullname", "location", "phone")
    search_fields = ("fullname", "location", "phone")
