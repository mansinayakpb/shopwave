"""
URL configuration for shopwave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
    # path('register/', views.RegisterView, name='register'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/", views.BuyerProfileView.as_view(), name="profile"),
    path("seller/profile/", views.SellerProfileView.as_view(), name="seller_profile"),
    path(
        "seller/dashboard/",
        views.SellerDashboardView.as_view(),
        name="seller_dashboard",
    ),
    path(
        "seller/create-product/",
        views.CreateProductBySellerView.as_view(),
        name="createproduct_seller",
    ),
    path("my-products/", views.SellerProductsView.as_view(), name="myproducts_seller"),
    path(
        "edit-product/<uuid:product_id>/",
        views.UpdateSellerProductView.as_view(),
        name="updateproduct_seller",
    ),
]
