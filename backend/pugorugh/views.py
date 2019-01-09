from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import mixins
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
    # lookup_field = 'pk'
    model = models.UserPref
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.UserPrefSerializer
    ## 1st 5 minutes of being awake
    # Now getting 200, 301 and 304 codes.
    # UserPrefs still failing to populate.
    queryset = models.UserPref.objects.all()

    def get_object(self):
        print('UserPref queryset: ', self.queryset)
        ## why is queryset an empty object?
        return get_object_or_404(
            self.queryset,
            user_id=self.kwargs.get('user_pk'),
            pk=self.kwargs.get('pk')
        )


class UserPrefViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer


class UserDogDetailView(RetrieveUpdateAPIView):
    '''
    Review or update each dog rating.
    '''
    model = models.UserDog


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer
