from django.contrib import admin

from .models import BotUser, ShoppingSession, CartItem


admin.site.register(BotUser)
admin.site.register(ShoppingSession)
admin.site.register(CartItem)
