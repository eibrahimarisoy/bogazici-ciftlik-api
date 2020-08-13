from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Category, Product

from .serializers import CategorySerializer, ProductSerializer


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
