from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serialize a category"""

    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """Serialize a product"""
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), 
    # )
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', \
             'distribution_unit', 'purchase_price', 'price']

        depth = 2
