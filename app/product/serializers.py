from rest_framework import serializers

from core.models import Category, Product

from django.shortcuts import get_object_or_404

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
        fields = ['id', 'category', 'name', \
             'distribution_unit', 'purchase_price', 'price']

    def get_distribution_unit(self, obj):
        return obj.get_distribution_unit_display()

    def create(self, validated_data):
        print(validated_data)

        print("1111111111111")
        category_dict = validated_data.pop('category')
        # distribution_unit_dict = validated_data.pop('distribution_unit')
        print(distribution_unit_dict)
        print("222222222222")
        category_obj, created = Category.objects.get_or_create(**category_dict)
        print("33333333333")
        return Product.objects.create(category=category_obj, **validated_data)