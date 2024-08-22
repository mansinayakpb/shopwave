from django import forms 
from .models import User, Profile, Category, Product, Order, OrderItem, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'category']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'user_type', 'email_verified', 'verification_code', 'is_approved']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer', 'total_price', 'is_paid', 'ordered_at']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['buyer']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    password2 = forms.CharField(
        label='Confirm Password (again)',
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'user_type']
        labels = {
            'email': 'Email',
            'user_type': 'Account Type',
        }


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
