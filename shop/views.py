from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import Category, Product, Cart, CartItem
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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

    def get(self, request, category_name=None):
        categories = Category.objects.all()
        products = Product.objects.all()

        if category_name:
            try:
                category = Category.objects.get(category_name=category_name)
                products = Product.objects.filter(category=category)
            except Category.DoesNotExist:
                products = Product.objects.none()  

        context = {
            'categories': categories,
            'products': products
        }
        return render(request, self.template_name, context)
    
    
class ProductView(TemplateView):
    template_name = 'product.html'

    def get(self, request, product_name=None):
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            product = Product.objects.none()
        
        context = {
            'product': product,
        }
        return render(request, self.template_name, context)


# class StoreView(TemplateView):
#     template_name = 'store.html'

#     def get(self, request, pk=None):
#         categories = Category.objects.all()
#         products = Product.objects.all()

#         if pk:
#             try:
#                 category = Category.objects.get(id=pk)
#                 products = Product.objects.filter(category=category)
#             except Category.DoesNotExist:
#                 products = Product.objects.none()

#         context = {
#             'categories': categories,
#             'products': products
#         }
#         return render(request, self.template_name, context)
    

# class ProductView(TemplateView):
#     template_name = 'product.html'

#     def get(self, request, category_pk=None, product_pk=None):
#         try:
#             category = Category.objects.get(id=category_pk)
#             product = Product.objects.get(id=product_pk, category=category)
#         except (Category.DoesNotExist, Product.DoesNotExist):
#             category = None
#             product = None

#         context = {
#             'category': category,
#             'product': product,
#         }

#         return render(request, self.template_name, context)




class CartView(TemplateView):
    template_name = 'cart.html'

    def get(self, request):
        cart = None
        cart_items = []

        try:
            cart = Cart.objects.get(buyer=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart = None

        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)


# SIGNUP


# class SignUpView(TemplateView):
#     template_name = 'signin/signin2.html'
#     # def get(self, request):
#     #     if request.user.is_authenticated:
#     #         return redirect('/')
#     #     form = SignUpForm()
#     #     return render(request, 'signin/signin2.html', {'form': form})
    
#     def post(self, request):
#         if request.user.is_authenticated:
#             return redirect('/')
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account Created Successfully!")
#             return redirect('/')
#         return render(request, self.template_name, {'form': form})

class SignUpView(TemplateView):
    template_name = 'signin/signin2.html'

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        
        # Handle GET request when there's no POST data
        if request.method == 'GET':
            form = SignUpForm()
        else:
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account Created Successfully!")
                return redirect('/')

        return render(request, self.template_name, {'form': form})




# Login


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_pass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully')
                    return redirect('/profile/')
                else:
                    form.add_error(None, 'Invalid username or password')
        else:
            form = AuthenticationForm()
        return render(request, 'signin/userlogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/profile/')


# profile


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'signin/profile.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')

# logout


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')



