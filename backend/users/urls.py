from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.users.api.views.user_sign_up import ClientUserSignUp
from backend.users.api.views.user_log_in import ClientUserLogIn
from backend.users.api.views.products import Products, NewProduct, ClientUserProducts
from backend.users.api.views.purchases import Purchases, NewPurchase

from backend.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]

router = DefaultRouter()

router.register("log-in", ClientUserLogIn, basename="log_in")
router.register("sign-up", ClientUserSignUp, basename="sign_up")
router.register("new-product", NewProduct, basename="new_product")
router.register("get-products", Products, basename="get_products")
router.register("get-user-products", ClientUserProducts, basename="get_user_products")
router.register("new-purchase", NewPurchase, basename="new_purchase")
router.register("get-purchases", Purchases, basename="get_purchases")

urlpatterns += [
    path("api/", include(router.urls)),
]
