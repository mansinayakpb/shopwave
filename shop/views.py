from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Category, Product
from .forms import CategoryForm, ProductForm


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


# class ProductView(TemplateView):
#     template_name = 'product-detail/product.html'

#     def get(self, request, **kwargs):
#         product_name = kwargs.get('product_name')
#         try:
#             product = Product.objects.get(product_name=product_name)
#         except Product.DoesNotExist:
#             product = None
        
#         context = {
#             'product': product,
#         }
#         return render(request, self.template_name, context)

