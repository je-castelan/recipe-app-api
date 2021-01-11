from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    """Serializes a tag object"""

    class Meta:
        model = models.Tag
        fields = ('id', 'name',)
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializes an ingredient object"""

    class Meta:
        model = models.Ingredient
        fields = ('id', 'name',)
        read_only_Fields = ('id',)
