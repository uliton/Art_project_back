from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .models import User, Artist


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password", "fullname")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "fullname"),
            },
        ),
    )
    list_display = ("email", "fullname", "is_staff")
    search_fields = ("email", "fullname")
    ordering = ("email",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("fullname", "location", "phone")
    search_fields = ("fullname", "location", "phone")

