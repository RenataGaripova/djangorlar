# Django modules
from django.db.models import (
    CharField,
    EmailField,
    DateField,
    BooleanField,
    DecimalField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Project modules
from .validators import validate_email_payload_not_in_full_name
from ..abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Manager for Custom User model."""
    def __obtain_user_instance(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, any],
    ) -> 'CustomUser':
        """Obtains user instance for creation."""

        if not email:
            raise ValidationError(
                message="Email can not be empty.",
                code='email_empty',
            )
        if not first_name and last_name:
            raise ValidationError(
                message="First name and last name can not be empty.",
                code="full_name_empty",
            )

        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )

        return new_user

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, any],
    ) -> 'CustomUser':
        """Creates a new user."""
        new_user = self.__obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, any],
    ) -> 'CustomUser':
        """Creates a new super user."""
        new_user = self.__obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """Custom User model."""

    MAX_EMAIL_LENGTH = 255
    MAX_NAME_LENGTH = 128
    PASSWORD_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 11
    CITY_MAX_LENGTH = 255
    SALARY_MAX_DIGITS = 12
    DECIMAL_PLACES = 2
    MAX_DEPARTMENT_LENGTH = 32
    MAX_ROLE_LENGTH = 32

    ROLES_CHOICES = (
        ("0", "Admin"),
        ("1", "Manager"),
        ("2", "employee"),
    )
    DEPARTMENT_CHOICES = (
        ("IT", "IT"),
        ("HR", "HR"),
        ("SLS", "Sales"),
        ("FNC", "Finiance"),
        ("MNG", "Management"),
    )
    email = EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name="Email address",
    )
    first_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="First name",
    )
    last_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Last name",
    )
    phone = CharField(
        max_length=PHONE_MAX_LENGTH,
        verbose_name="Phone number",
    )
    city = CharField(
        max_length=CITY_MAX_LENGTH,
        blank=True,
        verbose_name="City",
    )
    country = CharField(
        max_length=CITY_MAX_LENGTH,
        blank=True,
        verbose_name="Country",
    )
    department = CharField(
        max_length=MAX_DEPARTMENT_LENGTH,
        choices=DEPARTMENT_CHOICES,
        default="2",
        verbose_name="Department",
    )
    birth_date = DateField(
        verbose_name="Birthday",
        null=True,
    )
    salary = DecimalField(
        max_digits=SALARY_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        blank=True,
        verbose_name="Salary",
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        validators=[validate_password],
        verbose_name="Password",
        help_text="Hashed password",
    )
    is_active = BooleanField(
        verbose_name="Is user active?",
        default=True,
    )
    is_staff = BooleanField(
        verbose_name="Is staff?",
        default=False,
    )
    date_joined = DateField(
        auto_now_add=True,
        verbose_name="Date joined",
    )
    last_login = DateField(
        auto_now=True,
        null=True,
        verbose_name="last_login",
    )
    role = CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=ROLES_CHOICES,
        default="2",
        verbose_name="Role",
    )

    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-email"]

    def clean(self) -> None:
        """Validate user object before saving"""
        validate_email_payload_not_in_full_name(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        return super().clean()
