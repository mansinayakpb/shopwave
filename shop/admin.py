from django.contrib import admin
from .models import Category, User, Product, OrderItem, Profile, Order, Cart, CartItem

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description', 'cat_image')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'user_type', 'email_verified', 
                    'verification_code', 'is_approved')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'user', 'phone_number', 'address_line_1',
                    'address_line_2', 'city', 'state', 'postal_code',
                    'country')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'product_name', 'category', 'seller',
                    'description', 'price', 'stock', 'size', 'image')
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'order', 'product', 'price', 'quantity')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_dispaly = ('product', 'price', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'buyer')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'cart', 'product', 'quantity')