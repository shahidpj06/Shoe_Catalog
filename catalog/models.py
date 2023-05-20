from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=2083, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    gift_wrapped = models.BooleanField()

    def _str_(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

    def __str__(self):
        return self.name
