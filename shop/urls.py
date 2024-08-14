from django.urls import path
from .views import Home, StoreView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [    
    path('', Home.as_view(), name='home'),
    path('store/', StoreView.as_view(), name='storeview'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


