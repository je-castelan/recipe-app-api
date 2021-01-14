from rest_framework import viewsets, mixins
from recipe import serializers
from core.models import Tag, Ingredient, Recipe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BaseRecipeView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """Define a generic ViewSet for Ingredients and Tags"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """Return only the tags from the logged user"""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-name')

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user.
        More info here
        https://www.django-rest-framework.org/api-guide/generic-views/
        """
        serializer.save(user=self.request.user)


class TagView(BaseRecipeView):
    """Create a new tag for an user"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientView(BaseRecipeView):
    """Create a new ingredient for an user"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeView(viewsets.ModelViewSet):
    """Manage recipe"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user.
        More info here
        https://www.django-rest-framework.org/api-guide/generic-views/
        """
        serializer.save(user=self.request.user)
