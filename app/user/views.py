from rest_framework import authentication, generics, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import City, District, Neighborhood

from .serializers import (AuthTokenSerializer, CitySerializer,
                          DistrictSerializer, NeighborhoodSerializer,
                          UserSerializer)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CreateUserView(generics.CreateAPIView):
    """Create new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = DistrictSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class NeighborhoodViewSet(viewsets.ModelViewSet):
    queryset = Neighborhood.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = NeighborhoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)