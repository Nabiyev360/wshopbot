from django.db import models

from products.models import *


class BotUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    telephone = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class ShoppingSession(models.Model):
    STATUS_VARS = [
        (1, "Empty"),
        (2, "Active"),
        (3, "Purchased"),
    ]

    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=True)
    status = models.PositiveSmallIntegerField(("status"), choices=STATUS_VARS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.STATUS_VARS[self.status-1][1] + ' ' + str(self.total_price)


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.quantity) + ' ta | ' + self.product_id.title + ' | ' + self.session_id.user.first_name
