from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Category, Product, Cart, CartItem
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# from django.views import View

# class Home(TemplateView):
#     template_name = "home.html"

#     def get(self, request):
#         return render(request, self.template_name)


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, self.template_name, context)


class StoreView(TemplateView):
    template_name = 'store.html'

    def get(self, request):
        category_name = request.GET.get('category')
        
        if category_name:
            # Ensure we're matching with the correct field name `category_name`
            category = Category.objects.filter(category_name=category_name).first()
            products = Product.objects.filter(category=category) 
        else:
            products = Product.objects.all()

        categories = Category.objects.all()

        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, self.template_name, context)


class ProductView(TemplateView):
    template_name = 'product.html'

    def get(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        context = {
            'product': product,
        }
        return render(request, self.template_name, context)


class CartView(TemplateView):
    template_name = 'cart.html'

    def get(self, request):
        cart = Cart.objects.filter(buyer=request.user).first()
        cart_items = CartItem.objects.filter(cart=cart)

        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)

# SIGNUP


class SignUpView(TemplateView):
    template_name = 'signin/register.html'

    def get(self, request, *args, **kwargs):
        # Render the registration form
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return redirect('/')
        
        # Re-render the form with validation errors if form is not valid
        return render(request, self.template_name, {'form': form})

# Login


class UserLoginView(TemplateView):
    template_name = 'signin/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
        
        return render(request, self.template_name, {'form': form})


# profile


class UserProfileView(TemplateView):
    template_name = 'signin/profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'name': request.user})
        else:
            return redirect('/login/')


# logout


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


