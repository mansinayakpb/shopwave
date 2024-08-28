from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Category, Product, Cart, CartItem, Profile, Order, OrderItem
from .forms import SignUpForm, BuyerForm, SellerForm, SellerDashboardForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


# **************************************Authentication*****************************************************

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

# logout


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# ********************************************* Profile***************************************************


class BuyerProfileView(TemplateView, View):
    template_name = 'buyer/buyer_profile.html'

    def get(self, request):

        if request.user.user_type != "Buyer":
            return redirect('seller_profile')

        user_profile = Profile.objects.filter(user=request.user).first()
        if not user_profile:
            user_profile = Profile(user=request.user)
            user_profile.save()
        
        form = BuyerForm(instance=user_profile)
        context = {
            'form': form,
            'form_action': 'profile'
           
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.filter(user=request.user).first()
        buyer_form = BuyerForm(data=request.POST, instance=user_profile)
        if buyer_form.is_valid():
            buyer_form.save()

        return redirect('profile')


class SellerProfileView(TemplateView, View):
    template_name = 'seller/profile.html'

    def get(self, request):

        if request.user.user_type != "Seller":
            return redirect('profile')

        seller_profile = Profile.objects.filter(user=request.user).first()
        if not seller_profile:
            seller_profile = Profile(user=request.user)
            seller_profile.save()
        
        form = SellerForm(instance=seller_profile)
        context = {
            'form': form,
            'form_action': 'seller'
           
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        seller_profile = Profile.objects.filter(user=request.user).first()
        seller_form = SellerForm(data=request.POST, instance=seller_profile)
        if seller_form.is_valid():
            seller_form.save()

        return redirect('seller')

# ***********************************************Dashboard************************************************************

# Buyer Dashboard


class BuyerDashboardView(TemplateView):
    template_name = 'buyer/dashboard_buyer.html'

    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.filter(user=request.user).first()

        if user_profile and user_profile.choice == 'Buyer':
            context = {
                'profile': user_profile,
            }
        else:
            context = {}

        return self.render_to_response(context)

# seller Dashboard


class SellerDashboardView(TemplateView):
    template_name = 'seller/dashboard_seller.html'

    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.filter(user=request.user).first()
        if not user_profile:
            messages.error(request, "You are not authorized to view this page.")
            return redirect('/')

        context = {
            'seller_profile': user_profile,
        }
        return self.render_to_response(context)


class CreateProductBySellerView(TemplateView):
    template_name = 'seller/createproduct_seller.html'

    def get(self, request):
        if request.method == "GET":
            form = SellerDashboardForm()
        context = {
            'form': form,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SellerDashboardForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, "Product created successfully!")
                return redirect('seller_dashboard')
            else:
                messages.error(request, "There was an error with your submission.")
        else:
            form = SellerDashboardForm()

        context = {
            'form': form,
        }
        return self.render_to_response(context)



class SellerProductsView(TemplateView):
    template_name = 'seller/myproduct_seller.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(seller=request.user)
        return render(request, self.template_name, {'products': products})


class UpdateSellerProductView(View):
    template_name = 'seller/createproduct_seller.html'

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            messages.error(request, "Product not found.")
            return redirect('myproducts_seller')
        
        form = SellerDashboardForm(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            messages.error(request, "Product not found.")
            return redirect('myproducts_seller')
        
        form = SellerDashboardForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('myproducts_seller')
        else:
            messages.error(request, 'There was an error with your submission.')
        
        return render(request, self.template_name, {'form': form, 'product': product})


# Buyer Dashboard





# Home Page

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


# Details of the Product

class ProductView(TemplateView):
    template_name = 'product.html'

    def get(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        context = {
            'product': product,
        }
        return render(request, self.template_name, context)


# Store Page


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

# ************************************************Cart**************************************************
# Display the Cart Page


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
    

# Add the product into the cart

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


# Add the quantity of the product

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
    

# Remove the items from the cart

class RemoveView(TemplateView):
    def post(self, request, item_id):
        item = CartItem.objects.filter(id=item_id).first()

        if item:
            item.delete()
            messages.success(request, 'item removed successfully')
        else:
            messages.error(request, 'item does not exist')

        return redirect('cart_view')

# *********************************************order***************************************************

# order page review the cart items

class OrderView(TemplateView):
    template_name = 'place-order.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to place an order')
            return redirect('login')
        
        cart = Cart.objects.filter(buyer=request.user).first()
        if not cart:
            messages.error(request, 'No cart found for user')
            return redirect('cart_view')
        
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            messages.error(request, 'Your cart is empty')
            return redirect('cart_view')
        
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        
        if 'place_order' in request.GET:
            # Handle the order placement
            order = Order.objects.create(
                buyer=request.user,
                total_price=total_price,
                is_paid=False,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()

            messages.success(request, 'Your order has been placed successfully')
            return redirect('/')
        
        return self.render_to_response(context)

