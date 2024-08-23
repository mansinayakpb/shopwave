from django.urls import path
from .views import Home, StoreView, ProductView, CartView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [    
    path('', Home.as_view(), name='home'),
    path('store/', StoreView.as_view(), name='store'),
    path('product/<uuid:pk>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart_view'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)