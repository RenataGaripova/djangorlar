from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Address(models.Model):
    """Address model."""

    city = models.CharField(max_length=256, verbose_name="Город")
    street = models.CharField(max_length=256, verbose_name="Улица")
    house_number = models.IntegerField(verbose_name="Номер дома")
    additional_info = models.TextField(
        verbose_name="Дополнительная информация"
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "Адреса"
        default_related_name = "adresses"


class Cuisine(models.Model):
    """Cuisine model."""

    name = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "кухня"
        verbose_name_plural = "Кухни"


class Restaurant(models.Model):
    """Restaurant model."""

    name = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    cuisine = models.ForeignKey(
        to=Cuisine,
        on_delete=models.SET_NULL,
        null=True,
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "Рестораны"
        default_related_name = "restaurants"


class MenuItem(models.Model):
    """Menu item model."""

    name = models.CharField(max_length=128, verbose_name="Название")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    price = models.DecimalField(
        verbose_name="Цена",
        validators=[MinValueValidator(0.99)],
        decimal_places=2,
        max_digits=10,
    )
    is_available = models.BooleanField()
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
    )
    options = models.ManyToManyField(
        to="Option",
        through="Option_Item",
    )

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["price"]
        default_related_name = "menu_items"


class Category(models.Model):
    """Item category model."""

    name = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    menu_items = models.ManyToManyField(to=MenuItem, through="Category_Item")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Category_Item(models.Model):
    """Category to menu item relationship."""

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
    )
    menu_item = models.ForeignKey(
        to=MenuItem,
        on_delete=models.CASCADE,
    )
    position = models.IntegerField(verbose_name="Позиция")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('category', 'menu_item'),
                name="unique_category_item_pair"
            )
        ]


class Option(models.Model):
    """Option model."""

    name = models.CharField(max_length=128, verbose_name="Название")

    class Meta:
        verbose_name = "опция"
        verbose_name_plural = "Опции"


class Option_Item(models.Model):
    """Option to menu item relationship."""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
    )
    menu_item = models.ForeignKey(
        to=MenuItem,
        on_delete=models.CASCADE,
    )
    price_delta = models.DecimalField(
        verbose_name="Разница в цене",
        decimal_places=2,
        max_digits=10,
    )
    is_default = models.BooleanField(verbose_name="По умолчанию?")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('option', 'menu_item'),
                name="unique_option_item_pair"
            )
        ]
