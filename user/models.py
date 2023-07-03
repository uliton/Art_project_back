from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _

from gallery_app.models import Category
from user.validators import UnicodeFullnameValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field, but with fullname"""

    use_in_migrations = True

    def _create_user(self, email, password, fullname, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, fullname=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        # extra_fields.pop("first_name", None)
        # extra_fields.pop("last_name", None)
        return self._create_user(email, password,  fullname, **extra_fields)

    def create_superuser(self, email, password, fullname=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # extra_fields.pop("first_name", None)
        # extra_fields.pop("last_name", None)

        return self._create_user(email, password, fullname, **extra_fields)


class User(AbstractUser):
    username = None
    fullname_validator = UnicodeFullnameValidator()
    email = models.EmailField(_("email address"), unique=True)
    fullname = models.CharField(
        _("fullname"),
        max_length=30,
        help_text=_(
            "Required field.Min 5,max 30 symbols.Accepts Latin letters, spaces, hyphen (-), apostrophe (’)"
        ),
        validators=[fullname_validator],
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    objects = UserManager()



