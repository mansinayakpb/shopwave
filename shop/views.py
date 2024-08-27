from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Category, Product, Cart, CartItem, Profile
from .forms import SignUpForm, BuyerForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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

        total_price = 0.0
        tax_rate = 0.10
        for item in cart_items:
            item.total_price = float(item.product.price) * float(item.quantity)
            total_price += item.total_price

        tax = total_price * tax_rate
        final_total = total_price + tax

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'tax': tax,
            'final_total': final_total,
        }
        return render(request, self.template_name, context)
    

class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(id=product_id).first()

        if product:
            cart = Cart.objects.filter(buyer=request.user).first()
            if not cart:
                cart = Cart(buyer=request.user)
                cart.save()

            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if not cart_item:
                cart_item = CartItem(cart=cart, product=product, quantity=1)
                cart_item.save()
            else:
                cart_item.quantity += 1
                cart_item.save()

        return redirect('cart_view')


class QuantityView(TemplateView):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        quantity_action = request.POST.get('quantity_action')

        cart_item = CartItem.objects.filter(id=cart_item_id).first()

        if cart_item:
            if quantity_action == 'increase':
                cart_item.quantity += 1
            elif quantity_action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1

            cart_item.save()

        return redirect('cart_view')
    

class RemoveView(TemplateView):
    def post(self, request, item_id):
        item = CartItem.objects.filter(id=item_id).first()

        if item:
            item.delete()
            messages.success(request, 'item removed successfully')
        else:
            messages.error(request, 'item does not exist')

        return redirect('cart_view')








        

        


       










# SIGNUP

class SignUpView(TemplateView):
    template_name = 'signin/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/') 

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return redirect('/')
        
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


# class UserProfileView(TemplateView):
#     template_name = 'signin/profile.html'

#     def get(self, request):
#         if request.user.is_authenticated:
#             return render(request, self.template_name, {'name': request.user})
#         else:
#             return redirect('/login/')

class UserProfileView(TemplateView):
    template_name = 'signin/profile.html'

    def get(self, request):
        user_profile = Profile.objects.filter(user=request.user).first()
        if not user_profile:
            user_profile = Profile(user=request.user)
            user_profile.save()
        
        form = BuyerForm(instance=user_profile)
        context = {
            'form': form
           
        }
        return render(request, self.template_name, context)

    

# logout


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')



