from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Dog, UserDog, UserPref
from .serializers import UserSerializer, UserPrefSerializer, DogSerializer 
from .utils import get_age_range


class UserRegisterView(generics.CreateAPIView):
    '''
    Creates a new user and a new UserPref object to store their preferences.
    '''
    permission_classes = (permissions.AllowAny,)
    # AllowAny needed here, to create new user.
    model = get_user_model()

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserPref.create_default_pref(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    '''
    Allows authenticated user to update their UserPref.
    '''
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def put(self, request, *args, **kwargs):
        user_pref = self.get_object()
        serializer = UserPrefSerializer(user_pref, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDogLikedView(generics.UpdateAPIView):
    '''
    View for when user likes a dog.
    Sets UserDog status to 'l'.
    
    pk: the dog being liked.
    '''
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, created = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={'user': self.request.user,
                      'dog': dog,
                      'status': 'l'}
        )
        obj.status = 'l'
        obj.save()
        return Response("updated to liked", status=status.HTTP_200_OK)


class UserDogLikedNextView(generics.UpdateAPIView):
    '''
    Retrieves next dog from queryset of liked dogs.
    
    pk: the current dog in the list.
    '''
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            status='l',
        ).order_by('dog_id')

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        if not self.get_queryset():
            raise Http404
        user_dog = self.get_queryset().filter(dog_id__gt=dog_id).first()
        if user_dog is not None:
            return user_dog
        else:
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        user_dog = self.get_object()
        serializer = DogSerializer(user_dog.dog)
        return Response(serializer.data)


class UserDogDislikedView(generics.UpdateAPIView):
    '''
    View for when user dislikes a dog.
    Sets UserDog status to 'd'.
    
    pk: the dog being disliked.
    '''
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, created = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={'user': self.request.user,
                      'dog': dog,
                      'status': 'd'}
        )
        obj.status = 'd'
        obj.save()
        return Response("updated to disliked", status=status.HTTP_200_OK)


class UserDogDislikedNextView(generics.UpdateAPIView):
    '''
    Retrieves next dog from queryset of disliked dogs.
    
    pk: the current dog in the list.
    '''
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            status='d',
        ).order_by('dog_id')

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        if not self.get_queryset():
            raise Http404
        user_dog = self.get_queryset().filter(dog_id__gt=dog_id).first()
        if user_dog is not None:
            return user_dog
        else:
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        user_dog = self.get_object()
        serializer = DogSerializer(user_dog.dog)
        return Response(serializer.data)


class UserDogUndecidedView(generics.UpdateAPIView):
    '''
    View for when user is undecided about a dog.
    If UserDog object exists, deletes object,
    removing dog from liked/disliked list.

    pk: dog user is undecided on.
    '''
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        UserDog.objects.filter(
            user=self.request.user,
            dog=dog,
        ).delete()
        return Response("deleted", status=status.HTTP_200_OK)


class UserDogUndecidedNextView(generics.RetrieveAPIView):
    '''
    Retrieves next dog from queryset of dogs user hasn't decided on.
    Queryset excludes dogs that don't match UserPref attributes.

    pk: the current dog in the list.
    '''
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        '''
        Checks all dogs against user's preferences.
        Excludes dogs user has already sorted.
        '''
        user_pref = UserPref.objects.get(user=self.request.user)
        queryset = Dog.objects.filter(
            age__range=get_age_range(user_pref.age),
            gender__in=user_pref.gender,
            size__in=list(user_pref.size.split(","))
        ).exclude(
            Q(users_dog__user=self.request.user,
              users_dog__status='l') | Q(users_dog__user=self.request.user,
                                         users_dog__status='d')
        ).order_by('pk')
        return queryset

    def get_object(self):
        '''
        Find first relevant dog object after the current pk.
        '''
        dog_id = self.kwargs.get('pk')
        if not self.get_queryset():
            raise Http404
        dog = self.get_queryset().filter(id__gt=dog_id).first()
        if dog is not None:
            return dog
        else:
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = DogSerializer(dog)
        return Response(serializer.data)
        