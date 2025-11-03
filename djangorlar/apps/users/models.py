# Django modules
from django.db import models
from django.db.models import EmailField, CharField, BooleanField, DateField
from phone_field import PhoneField
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
# Project modules
from abstracts.models import AbstractBaseModel


class CustomUser(AbstractBaseUser):
    """Custom (base) User model."""
    MAX_USERNAME_LENGTH = 64
    MAX_EMAIL_LENGTH = 128
    MAX_NAME_LENGTH = 64

    username = CharField(
        unique=True,
        max_length=MAX_USERNAME_LENGTH,
        verbose_name="Unique usernmae",
        help_text="Create a unique and creative username",
    )
    email = EmailField(
        max_length=MAX_EMAIL_LENGTH,
        verbose_name="Email address",
        help_text="Enter a valid email address",
    )
    phone = PhoneField()
    is_active = BooleanField(
        verbose_name="Is active user?"
    )
    first_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="First name",
    )
    last_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Last name",
    )
    birth_date = DateField(
        verbose_name="User's birthday",
        help_text="Enter a birth date in a valid form."
    )

    class Meta:
        """Meta class for user model."""
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["id"]


class MyUser(AbstractUser):
    """Custom User model."""
    phone = PhoneField()
    is_active = BooleanField(
        verbose_name="Is active user?"
    )
    birth_date = DateField(
        verbose_name="User's birthday",
        help_text="Enter a birth date in a valid form."
    )

    class Meta:
        """Meta class for user model."""
        verbose_name = "My User"
        verbose_name_plural = "My Users"
        ordering = ["id"]
