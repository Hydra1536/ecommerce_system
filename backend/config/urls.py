"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from categories.views import CategoryViewSet
from config.views import *
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from orders.views import AdminDashboardView
from products.views import ProductViewSet
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API",
        default_version="v1",
        description="Ordering & Payment System API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
# router.register('orders', include('orders.urls'))
# router.register('payments', include('payments.urls'))
urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/", include(router.urls)),
    path("api/orders/", include("orders.urls")),
    path("api/categories/", include("categories.urls")),
    path("api/payments/", include("payments.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path("api/admin/dashboard/", AdminDashboardView.as_view()),
    path("", home),
    path("login/", login_page),
    path("register/", register_page),
    path("products/", products_page),
    path("cart/", cart_page),
    path("checkout/", checkout_page),
    path("orders/", orders_page),
    path("admin/dashboard/", admin_dashboard),
    path("admin/products/", admin_products),
    path("admin/orders/", admin_orders),
    path("admin/payments/", admin_payments),
    path(
        "admin/categories/", TemplateView.as_view(template_name="admin/categories.html")
    ),
]
