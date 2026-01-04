from django.shortcuts import render


def home(request):
    return render(request, "home.html")


# Auth
def login_page(request):
    return render(request, "auth/login.html")


def register_page(request):
    return render(request, "auth/register.html")


# User pages
def products_page(request):
    return render(request, "user/products.html")


def cart_page(request):
    return render(request, "user/cart.html")


def checkout_page(request):
    return render(request, "user/checkout.html")


def orders_page(request):
    return render(request, "user/orders.html")


# Admin pages
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")


def admin_products(request):
    return render(request, "admin/products.html")


def admin_orders(request):
    return render(request, "admin/orders.html")


def admin_payments(request):
    return render(request, "admin/payments.html")
