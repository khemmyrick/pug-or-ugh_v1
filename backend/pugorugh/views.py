from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPrefDetailView(RetrieveUpdateAPIView):
    '''
    Review or update user preferences.
    '''
    model = models.UserPref
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserDogDetailView(RetrieveUpdateAPIView):
    '''
    Review or update each dog rating.
    '''
    model = models.UserDog


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer
