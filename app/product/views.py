from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Category, Product

from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class ProductViewSet(viewsets.ModelViewSet):
    """Manage products in the  database"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('category', None)
        if name is not None:
            queryset = queryset.filter(category__name=name)
        return queryset