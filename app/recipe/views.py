from rest_framework import viewsets, mixins
from recipe import serializers
from core.models import Tag
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TagView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """Create a new user in the system"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()

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
