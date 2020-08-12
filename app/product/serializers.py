from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serialize a category"""

    class Meta:
        model = Category
        fields = ['id', 'name']