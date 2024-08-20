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
        categories = Category.objects.all()  # Fetch all categories from the database
        context = {'categories': categories}
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