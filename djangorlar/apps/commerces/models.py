from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from apps.catalogs.models import Restaurant, MenuItem, Address

User = get_user_model()

STATUS_CHOICES = (
    (0, "NEW"),
    (1, "CONFIRMED"),
    (2, "COOK"),
    (2, "DELIVERY"),
    (3, "DONE"),
)


class Order(models.Model):
    """Order model."""

    timestamp = models.DateTimeField(
        verbose_name="Время создания",
        auto_now_add=True,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=32,
        verbose_name="Статус"
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        to=Address,
        on_delete=models.SET_NULL,
        null=True
    )
    promocodes = models.ManyToManyField(
        to="PromoCode",
        through="Order_Promo",
    )
    subtotal = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Сумма без скидок",
        validators=[MinValueValidator(0.00)],
    )
    discount_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая скидка",
        validators=[MinValueValidator(0.00)],
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая сумма",
        validators=[MinValueValidator(0.00)],
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"
        default_related_name = "orders"


class Order_Item(models.Model):
    """Order to Item relationship."""

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        to=MenuItem,
        on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length=32, verbose_name="Название блюда")
    item_price = models.DecimalField(
        max_digits=10,
        verbose_name="Цена",
        validators=[MinValueValidator(0.99)],
        decimal_places=2,
    )
    quantity = models.IntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
    )

    def line_total(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "товар в заказе"
        verbose_name_plural = "Товары в заказе"
        default_related_name = "order_items"


class PromoCode(models.Model):
    """PromoCode model."""

    code = models.CharField(max_length=16, unique=True)
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Скидка в %",
        validators=[MinValueValidator(0.00)],
    )
    is_active = models.BooleanField("Действует сейчас?")

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "Промокоды"
        default_related_name = "promocodes"


class Order_Item_Option(models.Model):
    """Order Item to Option relationship."""

    order_item = models.ForeignKey(
        to=Order_Item,
        on_delete=models.CASCADE,
    )
    option_name = models.CharField(max_length=256, verbose_name="Название")
    price_delta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Разница в цене"
    )

    class Meta:
        verbose_name = "опция к товару"
        verbose_name_plural = "Опции к товару"
        default_related_name = "item_options"


class Order_Promo(models.Model):
    """Order Item to Option relationship."""

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
    )
    promocode = models.ForeignKey(
        to=PromoCode,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "промокод заказа"
        verbose_name_plural = "Промокоды заказа"
        default_related_name = "order_promocodes"
        constraints = [
            models.UniqueConstraint(
                fields=('order', 'promocode'),
                name="unique_promo_order_pair"
            )
        ]
