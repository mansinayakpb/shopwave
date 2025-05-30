import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from shop.managers import UserManager


class TimesStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(AbstractUser, TimesStampedModel):

    USER_TYPE_CHOICES = [
        ("Buyer", "Buyer"),
        ("Seller", "Seller"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="Buyer"
    )
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_verification_code(self):
        self.verification_code = str(uuid.uuid4())
        self.token_created_at = timezone.now()
        self.save()

    def is_token_valid(self):
        if self.token_created_at:
            return (
                timezone.now() - self.token_created_at
            ) < timezone.timedelta(hours=24)
        return False


class Profile(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    phone_number = models.BigIntegerField()
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True
    )
    # Buyer fields
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Seller Fields

    gst = models.CharField(max_length=255, blank=True, null=True)
    pan_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"


class Category(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255, unique=True)
    cat_image = models.ImageField(upload_to="static/", null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name


# class Product(TimesStampedModel):
#     SIZE_CHOICES = [
#         ("S", "S"),
#         ("M", "M"),
#         ("L", "L"),
#         ("XL", "XL"),
#         ("XXL", "XXL"),
#     ]
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     seller = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="seller_products"
#     )
#     category = models.ForeignKey(
#         "Category",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="category_products",
#     )
#     product_name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="M")
#     image = models.ImageField(upload_to="static/", null=True, blank=True)


#     def __str__(self):
#         return self.product_name
class Product(TimesStampedModel):
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_products"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="category_products",
    )
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="M")
    image = models.ImageField(upload_to="static/", null=True, blank=True)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=0, null=True, blank=True
    )
    discount_start_date = models.DateField(null=True, blank=True)
    discount_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    @property
    def discounted_price(self):
        """Calculate and return the discounted price if the discount is active."""
        if (
            self.discount_percentage
            and self.discount_start_date
            and self.discount_end_date
        ):
            today = timezone.now().date()
            if self.discount_start_date <= today <= self.discount_end_date:
                discount = Decimal(self.discount_percentage)
                return self.price - (self.price * discount / 100)
        return None


class Order(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.email}"


class OrderItem(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"


class Payment(TimesStampedModel):
    stripe_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.stripe_id} for order {self.order.id}"


class Cart(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart"
    )

    def __str__(self):
        return f"{self.buyer.email}'s cart"


class CartItem(TimesStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_products"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in cart"
