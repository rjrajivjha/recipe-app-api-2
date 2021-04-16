from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """

    serializer_class = AuthTokenSerializer
    """ this will make it a browsable API, we can see this in the browser"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
