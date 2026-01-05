from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.permissions import IsAdmin

from .models import Category
from .serializers import CategorySerializer
from .utils import dfs_category_tree


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class CategoryTreeView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        cached_tree = cache.get("category_tree")
        if cached_tree:
            return Response(cached_tree)

        roots = Category.objects.filter(parent=None)
        tree = [dfs_category_tree(cat) for cat in roots]
        cache.set("category_tree", tree, timeout=3600)
        return Response(tree)
