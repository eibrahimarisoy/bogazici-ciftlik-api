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
    category = CategorySerializer()
    distribution_unit = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_distribution_unit(self, obj):
        return obj.get_distribution_unit_display()


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
