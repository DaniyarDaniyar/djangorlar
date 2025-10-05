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
    PROTECT,
    CASCADE,
)

# Project modules


class Restaurant(Model):
    """Restaurant database (table) model."""

    NAME_MAX_LEN = 200

    name = CharField(
    max_length=NAME_MAX_LEN,
)
    description = TextField(
        blank=True,
        default="",
    )
    address = TextField(
        blank=True,
        default="",
    )
    is_active = BooleanField(
        default=True,
    )


class Category(Model):
    """Category database (table) model"""

    name = CharField(
        max_length=200,
    )


class Option(Model):
    """Oprion (table) model"""

    name = CharField(
        max_length=200,
    )

class MenuItem(Model):
    """ MenuItem database (table) model"""

    NAME_MAX_LEN = 200

    restaurant_id = ForeignKey(
        to=Restaurant,
        on_delete=CASCADE,
        related_name="menu_items",
    )

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    description = TextField(
        blank=True,
        default="",
    )
    price = DecimalField(
        max_digits=8, 
        decimal_places=2,
        default=0,
    )
    is_available = BooleanField(
        default=True,
    )
    categories = ManyToManyField(
        to=Category,
        through="ItemCategory",
        through_fields=("menu_item", "category"),
        related_name="menu_items",
    )
    options = ManyToManyField(
        to=Option,
        through="ItemOption",
        through_fields=("menu_item", "option"),
        related_name="menu_items",
    )

class ItemCategory(Model):
    """Through table for MenuItem-Category relation"""

    menu_item = ForeignKey(
        to=MenuItem,
        on_delete=CASCADE,
    )
    category = ForeignKey(
        to=Category,
        on_delete=CASCADE,
    )
    position = IntegerField(
        default=0,
    )

    class Meta:

        constraints = [
            UniqueConstraint(
                fields=["menu_item", "category"],
                name="unique_menu_item_and_category",
            ),
        ]

class ItemOption(Model):
    """Through table for MenuItem-Option relation"""

    menu_item = ForeignKey(
        to=MenuItem,
        on_delete=CASCADE,
    )
    option = ForeignKey(
        to=Option,
        on_delete=CASCADE,
    )
    price_delta = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    is_default = BooleanField(
        default=False,
    )

    class Meta:
        
        constraints = [
            UniqueConstraint(
                fields=["menu_item", "option"],
                name="unique_menu_item_and_option",
            ),
        ]
    
