from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.models import Product
from coupons.models import Coupon


class Order(models.Model):
    """
    Since 'verbose_name' is the 1st arg of 'Field' (parent class of Char..),
    you COULD write it like this: 'CharField(_("first_name"), max_length=50)'.
    """

    first_name = models.CharField(verbose_name=_("first_name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last_name"), max_length=50)
    email = models.EmailField(verbose_name=_("email"))
    address = models.CharField(verbose_name=_("address"), max_length=250)
    postal_code = models.CharField(
        verbose_name=_("postal_code"), max_length=25
    )
    city = models.CharField(verbose_name=_("city"), max_length=100)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Optional
    coupon = models.ForeignKey(
        to=Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)  # new to old, DESC

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        # items     OrderItems
        # get_cost  OrderItems's method 'get_cost'
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal("100"))


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product, related_name="order_items", on_delete=models.CASCADE
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "f{self.id}"

    def get_cost(self):
        return self.price * self.quantity
