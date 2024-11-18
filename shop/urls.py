from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (ActivateAccountView, AddToCartView, ApplyDiscountView,
                    BuyerDashboardView, BuyerProfileView, CartView,
                    ChangePasswordView, CreateProductBySellerView, Home,
                    OrderCompleteView, OrderHistoryView, OrderView,
                    ProductView, QuantityView, RemoveView, ResetCompleteView,
                    ResetConfirmView, ResetDoneView, ResetPasswordView,
                    SellerDashboardView, SellerProductsView, SellerProfileView,
                    SignUpView, StoreView, SuccessView,
                    UpdateSellerProductView, UserLoginView, UserLogoutView)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("store/", StoreView.as_view(), name="store"),
    path("product/<uuid:pk>/", ProductView.as_view(), name="product"),
    path("cart/", CartView.as_view(), name="cart_view"),
    path("addtocart/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/quantity/", QuantityView.as_view(), name="quantity_view"),
    path(
        "cart/remove/<uuid:item_id>/",
        RemoveView.as_view(),
        name="remove_from_cart",
    ),
    path("cart/placeorder/", OrderView.as_view(), name="order_place"),
    # path("success/", SuccessView.as_view(), name="success"),
    path("OrderComplete/", OrderCompleteView.as_view(), name="Order_Complete"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # path("googlelogout/", GoogleLogoutView.as_view(), name="Google"),
    path("buyer/profile/", BuyerProfileView.as_view(), name="buyer_profile"),
    path("OrderHistory/", OrderHistoryView.as_view(), name="Order_History"),
    path(
        "buyer/dashboard/",
        BuyerDashboardView.as_view(),
        name="buyer_dashboard",
    ),
    path(
        "seller/profile/", SellerProfileView.as_view(), name="seller_profile"
    ),
    path(
        "seller/dashboard/",
        SellerDashboardView.as_view(),
        name="seller_dashboard",
    ),
    path(
        "seller/create-product/",
        CreateProductBySellerView.as_view(),
        name="createproduct_seller",
    ),
    path(
        "my-products/", SellerProductsView.as_view(), name="myproducts_seller"
    ),
    path(
        "edit-product/<uuid:product_id>/",
        UpdateSellerProductView.as_view(),
        name="updateproduct_seller",
    ),
    path("success/", SuccessView.as_view(), name="success"),
    # email verification
    path(
        "activate/<str:uid>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    # Forgot password
    path("passwordreset/", ResetPasswordView.as_view(), name="password_reset"),
    path("resetdone/", ResetDoneView.as_view(), name="reset_done"),
    path(
        "resetconfirm/<uidb64>/<token>/",
        ResetConfirmView.as_view(),
        name="reset_confirm",
    ),
    path("resetcomplete/", ResetCompleteView.as_view(), name="reset_complete"),
    # Change password
    path(
        "changepassword/", ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "apply-discount/", ApplyDiscountView.as_view(), name="apply_discount"
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
