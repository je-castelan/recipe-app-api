from rest_framework import serializers

from core import models

from core.models import Ingredient, Tag


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


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serialize a recipe
    PrimaryKeyRelatedField only returns the id's with a relationship.
    https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
    """

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes', 'price',
            'link',
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """
    In this case, it will modify tags and ingredients with their detail
    """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
