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

    '''
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    userpref = models.UserPref(
        user=model,
        age='b',
        gender='f',
        size='s'
    )
    userpref.create()
    '''
    

class UserPrefDetailView(RetrieveUpdateAPIView):
    '''
    Review or update user preferences.
    '''
    model = models.UserPref
    lookup_field = 'pk'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.UserPrefSerializer
    user = self.request.user
    queryset = models.UserPref.objects.filter(user=self.user)

    def get_queryset(self):
        return models.UserPref.objects.filter(user=self.request.user)

    def get_object(self):
        print('UserPref queryset: ', self.queryset)
        ## print line displays ALL UserPref objects.
        ## No new UserPref objects made since adding signals...
        ## UserPref update logic must be added to app somewhere.
        # is this also returning a queryset?
        return get_object_or_404(
            self.queryset,
            user_id=self.kwargs.get('user_pk'),
            pk=self.kwargs.get('pk')
        )


    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    """


class UserPrefViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    # Does this need more attrs?  Should I use this at all?


class UserDogDetailView(RetrieveUpdateAPIView):
    '''
    Review or update each dog rating.
    '''
    model = models.UserDog


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer
