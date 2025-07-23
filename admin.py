from django.contrib import admin
from .models import Medicine, Product, CartItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'medicine', 'quantity')

    def get_user(self, obj):
        return obj.cart.user
    get_user.short_description = 'User'
