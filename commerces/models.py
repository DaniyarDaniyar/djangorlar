# Python modules + Third party modules

# Django modules
from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    TextField,
    IntegerField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    BooleanField,
    DecimalField,
    PositiveBigIntegerField,
    SET_NULL,
    PROTECT,
    CASCADE,
)

from django.contrib.auth.models import User
# Project modules
from catalogs.models import Restaurant, MenuItem


class Address(Model):
    """Address db (table)model"""

    CITY_MAX_LENGTH = 100
    POSTAL_CODE_MAX_LENGTH = 20
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="addresses",
    )
    line1 = TextField()
    city = CharField(
        max_length=CITY_MAX_LENGTH
    )
    postal_code = CharField(
        max_length=POSTAL_CODE_MAX_LENGTH
    )
    is_default = BooleanField(
        default=False
    )

class Order(Model):
    """Order db (table) model"""

    MAX_DIGITS = 10
    DECIMAL_PLACES = 2

    STATUS_NEW = 1
    STATUS_NEW_LABEL = "New"
    STATUS_CONFIRMED = 2
    STATUS_CONFIRMED_LABEL = "Confirmed"
    STATUS_DELIVERING = 3
    STATUS_DELIVERING_LABEL="Delivering"
    STATUS_DONE = 4
    STATUS_DONE_LABEL = "Done"
    STATUS_CHOICES = {
        STATUS_NEW: STATUS_NEW_LABEL,
        STATUS_CONFIRMED: STATUS_CONFIRMED_LABEL,
        STATUS_DELIVERING: STATUS_DELIVERING_LABEL,
        STATUS_DONE: STATUS_DONE_LABEL,
    }
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="orders",
    )
    restaurant = ForeignKey(
        to=Restaurant,
        on_delete=CASCADE,
        related_name="orders",
    )
    address = ForeignKey(
        to=Address,
        on_delete=CASCADE,
        related_name="orders",
    )
    status = IntegerField(
        default=STATUS_NEW,
        choices=STATUS_CHOICES,
    )
    subtotal = DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0,
    )
    discount_total = DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0,
    )
    total = DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0,
    )
    created_at = DateTimeField(
        auto_now_add=True,
    )

class OrderItem(Model):
    order = ForeignKey(
        to=Order,
        on_delete=CASCADE,
        related_name="items",
    )
    menu_item = ForeignKey(
        to=MenuItem,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    item_name = CharField(
        max_length=200
    )
    item_price = DecimalField(
        max_digits=8, 
        decimal_places=2,
    )
    quantity = PositiveBigIntegerField(
        default=1,
    )
    line_total = DecimalField(
        max_digits=10,
        decimal_places=2,
    )

class OrderItemOption(Model):
    order_item = ForeignKey(
        to=OrderItem,
        on_delete=CASCADE,
        related_name="options",
    )
    option_name = CharField(
        max_length=100,
    )
    price_delta = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

class PromoCode(Model):
    """PromoCode db (table) model."""
    code = CharField(
        max_length=100,
        unique=True,
    )
    description = TextField(
        blank=True,
        default="",
    )
    discount_percent = DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

class OrderPromo(Model):
    order = ForeignKey(
        to=Order,
        on_delete=CASCADE,
        related_name="order_promo",
    )
    promo = ForeignKey(
        to=PromoCode,
        on_delete=CASCADE,
        related_name="order_promo",
    )
    applied_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["order", "promo"],
                name="uniqe_order_promo",
            ),
        ]



