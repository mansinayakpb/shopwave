from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (Cart, CartItem, Category, Order, OrderItem, Payment,
                     Product, Profile, User)

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "description", "cat_image")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm  # Use the custom change form
    add_form = CustomUserCreationForm  # Use the custom creation form

    list_display = (
        "id",
        "email",
        "user_type",
        "email_verified",
        "verification_code",
        "is_approved",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "user_type",
                    "email_verified",
                    "verification_code",
                    "token_created_at",
                    "is_approved",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "user_type",
                    "password1",
                    "password2",
                    "is_approved",
                ),
            },
        ),
    )

    filter_horizontal = ("user_permissions", "groups")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_dispaly = (
        "id",
        "user",
        "phone_number",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "postal_code",
        "country",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_dispaly = (
        "id",
        "product_name",
        "category",
        "seller",
        "description",
        "price",
        "stock",
        "size",
        "image",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_dispaly = ("id", "order", "product", "price", "quantity")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_dispaly = ("product", "price", "quantity")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_dispaly = ("id", "buyer")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_dispaly = ("id", "cart", "product", "quantity")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "amount",
        "payment_method",
        "payment_status",
        "transaction_id",
    )
