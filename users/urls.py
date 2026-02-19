from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import PaymentListAPIView, PaymentViewSet, UserCreateAPIView

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payments")


app_name = UsersConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
