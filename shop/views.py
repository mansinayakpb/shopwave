from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Category, Product, Cart, CartItem
from .forms import SignUpForm, CategoryForm, ProductForm
from django.contrib import messages

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
    template_name = 'stores/store.html'

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
    template_name = 'product-detail/product.html'

    def get(self, request, product_name=None):
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            product = Product.objects.none()
        
        context = {
            'product': product,
        }
        return render(request, self.template_name, context)


class CartView(TemplateView):
    template_name = 'cart/cart.html'

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


class SignUpView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm()
        return render(request, 'signin/signin.html', {'form': form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return redirect('/')
        return render(request, 'signin/signin.html', {'form': form})


    






# def sign_up(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             messages.success(request, "Account Created Successfully!!")
#             form.save()
#     else:
#         form = SignUpForm()
#     return render(request, 'enroll/signup.html', {'form': form})
    
