from rest_framework import generics
from user import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserProfileSerializer


class UserLoginApiViewv1(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserLoginApiViewv2(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = serializers.AuthTokenSerializer


class RetrieveUserView(generics.RetrieveUpdateAPIView):
    """Create a new user in the system"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def get_object(self):
        return self.request.user
