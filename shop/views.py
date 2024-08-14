from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Category, Product
from .forms import CategoryForm, ProductForm


class Home(TemplateView):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)


class StoreView(TemplateView):
    template_name = 'stores/store.html'

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, self.template_name, context)


class CreateCategory(TemplateView):
    template_name = ''

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("")
        else:
            form = CategoryForm()
        return render(request, self.template_name, {"form": form})
    

class UpdateCategory(TemplateView):
    template_name = ''

    def get(self, request, pk):
        category = Category.objects.filter(id=pk).first()
        if category:
            form = CategoryForm(instance=category)
            return render(request, self.template_name, {'form': form})
        # else:
        #     # return HttpResponse("")

    def post(self, request, pk):
        category = Category.objects.filter(id=pk).first()
        if category:
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return render(request, self.template_name, {'form': form})
            else:
                return render(request, self.template_name, {'form': form})
            

class ViewCategory(TemplateView):
    template_name = ''

    def get(self, request, pk):
        category = Category.objects.filter(id=pk).first()
        if category:
            return render(request, self.template_name, {"category": category})
        # else:
        #     # return HttpResponse("Post not found.")


# class DeleteCategory(TemplateView):
#     template_name = ''

#     def post(self, request, pk):
#         category = Category.objects.get(id=pk)
#         if category:
#             category.delete()
#             return redirect('')
#         return render(request, self.template_name, {'category': category})
    

class CreateProduct(TemplateView):
    template_name = ''

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("")
        else:
            form = ProductForm()
        return render(request, self.template_name, {"form": form})
    

class UpdateProduct(TemplateView):
    template_name = ''

    def get(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if product:
            form = ProductForm(instance=product)
            return render(request, self.template_name, {'form': form})
        # else:
        #     # return HttpResponse("")

    def post(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if product:
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return render(request, self.template_name, {'form': form})
            else:
                return render(request, self.template_name, {'form': form})