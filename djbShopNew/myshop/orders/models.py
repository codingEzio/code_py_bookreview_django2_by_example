from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)  # new to old, DESC

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        # items     OrderItems
        # get_cost  OrderItems's method 'get_cost'
        return sum(item.get_cost() for item in self.items.all())


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
