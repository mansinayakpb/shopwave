from django import forms
from .models import (
    User,
    Profile,
    Category,
    Product,
    Order,
    OrderItem,
    Cart,
    CartItem,
)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "description", "price", "category"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "user_type",
            "email_verified",
            "verification_code",
            "is_approved",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["buyer", "total_price", "is_paid", "ordered_at"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity", "price"]


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["buyer"]


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "user_type",
            "password1",
            "password2",
        ]
        labels = {
            "email": "Email",
            "user_type": "Account Type",
        }


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


# Profile forms for Buyer and Seller


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "state",
            "city",
            "address_line_1",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Country"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address Line 1",
                }
            ),
        }


class SellerForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "gst",
            "pan_number",
            "phone_number",
            "country",
            "state",
            "city",
            "address_line_1",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "gst": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "GST Number"}
            ),
            "pan_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "PAN Number"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Country"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address Line 1",
                }
            ),
        }


# form tp create product by seller in dashboard


class SellerDashboardForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            "category",
            "product_name",
            "description",
            "price",
            "stock",
            "size",
            "image",
            "price",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
