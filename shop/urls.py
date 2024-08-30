from django.urls import path
from .views import Home, StoreView, ProductView, CartView, AddToCartView, QuantityView, RemoveView, OrderView, PaymentProcessView, PaymentSuccess, PaymentCancel
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('store/', StoreView.as_view(), name='store'),
    path('product/<uuid:pk>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('addtocart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/quantity/', QuantityView.as_view(), name='quantity_view'),
    path('cart/remove/<uuid:item_id>/', RemoveView.as_view(), name='remove_from_cart'),
    path('cart/placeorder/', OrderView.as_view(), name='order_place'),
    path('payment/process/', PaymentProcessView.as_view(), name='payment_process'),
    # path('success/', success_view, name='success_page'),
    # path('cancel/', cancel_view, name='cancel_page'),

    path("payment-success/", PaymentSuccess, name="payment-success"),
    path("payment-cancel/", PaymentCancel, name="payment-cancel"),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
