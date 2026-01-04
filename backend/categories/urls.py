from django.urls import path

from .views import CategoryTreeView

urlpatterns = [
    path("categories/tree/", CategoryTreeView.as_view()),
]
