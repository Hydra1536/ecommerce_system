from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response  

from rest_framework.viewsets import ModelViewSet

from .models import Product
from .permissions import IsAdmin
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]
