from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)
from . import views
from . import models
from .utils import get_age_range
from .serializers import DogSerializer, UserSerializer, UserPrefSerializer


# Create your tests here.
class UserZero(object):
    """
    A setUp object for UserRegTests.
    """
    def setUp(self):
        self.user0 = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='p4ssw0rd'
        )
        self.user0.save()
        
        auth = self.client.post('/api-token-auth/', 
                                {'username': 'test_user',
                                 'email': 'test@example.com',
                                 'password': 'p4ssw0rd'})
        token = auth.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class Pregame(object):
    """
    Setup to repeat for all tests in a TestCase.

    Creates sample Dog, UserDog, UserPref and User objects.
    Creates sample context dictionaries for certain Menu and Item objects.
    """
    def setUp(self):

        # Request factory.
        self.factory = APIRequestFactory()

        # Sample Dogs.
        self.dog1 = models.Dog(
            name='Dog1',
            image_filename='dog1.png',
            breed='dog1',
            age=2,
            gender='m',
            size='xl',
        )
        self.dog1.save()
        self.dog2 = models.Dog(
            name='Dog2',
            image_filename='dog2.png',
            breed='dog2',
            age=36,
            gender='f',
            size='l',
        )
        self.dog2.save()
        self.dog3 = models.Dog(
            name='Dog3',
            image_filename='dog3.png',
            breed='dog3',
            age=96,
            gender='m',
            size='s',
        )
        self.dog3.save()

        # Sample Users.
        self.user1 = User.objects.create_user(
            'User1',
            'user1@example.com',
            'all0fthebikes'
        )
        self.user1.save()
        self.user2 = User.objects.create_user(
            'User2',
            'user2@example.com',
            'kimora1ex'
        )
        self.user2.save()
        self.user3 = User.objects.create_user(
            'User3',
            'user3@example.com',
            'sixmilliondollar5man'
        )
        self.user3.save()

        # Sample UserPrefs.
        self.userpref1 = models.UserPref(
            user=self.user1,
            age='y',
            gender='m',
            size='m',
        )
        self.userpref1.save()
        self.userpref2 = models.UserPref(
            user=self.user2,
            age='a,s',
            gender='f',
            size='l',
        )
        self.userpref2.save()
        self.userpref3 = models.UserPref(
            user=self.user3,
            age='b',
            gender='f',
            size='m',
        )
        self.userpref3.save()

        # Sample UserDog Relationship Instances.
        self.userdog1 = models.UserDog(
            user=self.user1,
            dog=self.dog2,
            status='l'
        )
        self.userdog1.save()
        self.userdog2 = models.UserDog(
            user=self.user2,
            dog=self.dog1,
            status='l'
        )
        self.userdog2.save()
        self.userdog3 = models.UserDog(
            user=self.user3,
            dog=self.dog2,
            status='d'
        )
        self.userdog3.save()
        self.userdog4 = models.UserDog(
            user=self.user1,
            dog=self.dog3,
            status='l'
        )
        self.userdog4.save()


class PugOrUghModelTests(Pregame, TestCase):
    '''Pug-or-ugh model tests.'''
    def test_dog_creation(self):
        '''A sample dog is created successfully.'''
        self.assertEqual(self.dog1.name, 'Dog1')
        self.assertNotEqual(self.dog1.gender, self.dog2.gender)
        self.assertLessEqual(self.dog3.created_at, timezone.now())
        
    def test_user_pref_creation(self):
        '''A sample user preferences profile is created successfully.'''
        self.assertEqual(self.userpref1.user, self.user1)
        self.assertNotEqual(self.userpref2.user, self.user3)
        self.assertLessEqual(self.userpref3.created_at, timezone.now())
        
    def test_user_dog_creation(self):
        '''A sample relationship object is created for a user and dog.'''
        self.assertEqual(self.userdog1.status, 'l')
        self.assertNotEqual(self.userdog2.dog, self.dog2)
        self.assertLessEqual(self.userdog2.created_at, timezone.now())


class UserRegTests(UserZero, APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        New UserPref object is simultaneously created.
        """
        new_data = {'username': 'new_user',
                    'email': 'newuser@example.com',
                    'password': 'bendtheKnee806GoT'}
        url = reverse('register-user')
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        # setUp user0 plus new_user == 2
        # check user via username.  email and/or password may not be available for testing suite?
        self.assertEqual(User.objects.get(username='new_user').username,
                         'new_user')
        user_pref = models.UserPref.objects.get(user=User.objects.get(username='new_user'))
        self.assertNotEqual(user_pref, None)
        self.assertEqual(user_pref.age, 'b')


class PugOrUghViewTests(Pregame, TestCase):
    '''Pug-or-ugh view tests.'''
    def test_retrieve_update_user_pref_view(self):
        view = views.RetrieveUpdateUserPrefView.as_view()
        user = self.user3
        data = {'id': user.id,
                'age': 's',
                'gender': self.dog1.gender,
                'size': self.dog1.size}
        request = self.factory.put('/api/user/preferences/', data=data)
        force_authenticate(request, user=user)
        resp = view(request)
        self.assertNotEqual(resp.status_code, 401)
        self.assertEqual(resp.status_code, 200)

    def test_retrieve_update_user_pref_view_unauth(self):
        view = views.RetrieveUpdateUserPrefView.as_view()
        user = self.user3
        data = {'id': user.id,
                'age': 's',
                'gender': self.dog1.gender,
                'size': self.dog1.size}
        request = self.factory.put('/api/user/preferences/', data=data)
        resp = view(request)
        self.assertEqual(resp.status_code, 401)

    def test_user_dog_liked_view_bad(self):
        view = views.UserDogLikedView.as_view()
        user = self.user3

        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '-1'}))
        force_authenticate(request, user=user)
        resp = view(request)
        self.assertEqual(resp.status_code, 404)

    def test_user_dog_liked_view(self):
        '''
        Test UserDogLikedView
        '''
        view = views.UserDogLikedView.as_view()
        user = self.user3
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '2'}))
        # self.dog2.pk is 2. Signed in user is user in question.
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        self.userdog3.refresh_from_db()
        self.userdog3.save()
        # This response is HTML, not json.
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, "updated to liked")
        self.assertNotEqual(self.userdog3.status, 'd')
        self.assertEqual(self.userdog3.status, 'l')

    def test_user_dog_disliked_view(self):
        '''
        Test UserDogDislikedView
        '''
        view = views.UserDogDislikedView.as_view()
        user = self.user1
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '2'}))
        # self.dog2.pk is 2. Signed in user is user in question.
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        self.userdog1.refresh_from_db()
        self.userdog1.save()
        # This response is HTML, not json.
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, "updated to disliked")
        self.assertNotEqual(self.userdog1.status, 'l')
        self.assertEqual(self.userdog1.status, 'd')

    def test_user_dog_undecided_view(self):
        '''
        Test UserDogUndecidedView
        '''
        view = views.UserDogUndecidedView.as_view()
        user = self.user1
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '2'}))
        # self.dog2.pk is 2. Signed in user is user in question.
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        self.assertRaises(ObjectDoesNotExist, self.userdog1.refresh_from_db)
        # self.userdog1 is successfully deleted.
        # This response is HTML, not json.
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, "deleted")

    def test_user_dog_undecided_next_view(self):
        view = views.UserDogUndecidedNextView.as_view()
        user = self.user2
        next_dog = self.dog2
        not_next = self.dog3
        serializer = DogSerializer(instance=next_dog)
        serializer2 = DogSerializer(instance=not_next)
        request = self.factory.get(reverse('dog-undecided-next',
                                           kwargs={'pk': '2'}))
        # user2 only liked dog1.  Dog3 is outside bounds of user2's prefs.
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        self.assertEqual(resp.data, serializer.data)
        self.assertNotEqual(resp.data, serializer2.data)
        # AssertNotEqual makes sure UserPref is working.

    def test_user_dog_disliked_next_view(self):
        view = views.UserDogDislikedNextView.as_view()
        user = self.user3
        next_dog = self.dog2
        serializer = DogSerializer(instance=next_dog)
        request = self.factory.get(reverse('dog-disliked-next',
                                           kwargs={'pk': '2'}))
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        # user3 has only disliked dog2, so next_dog is still dog2.
        self.assertEqual(resp.data, serializer.data)

    def test_user_dog_liked_next_view(self):
        view = views.UserDogLikedNextView.as_view()
        user = self.user1
        next_dog = self.dog3
        serializer = DogSerializer(instance=next_dog)
        request = self.factory.get(reverse('dog-liked-next',
                                           kwargs={'pk': '2'}))
        force_authenticate(request, user=user)
        resp = view(request, pk='2')
        # user1 liked dogs 2 and 3.  next_dog is dog3.
        self.assertEqual(resp.data, serializer.data)


class PugOrUghUtilsTest(TestCase):
    '''Pug-or-Ugh utils test.'''
    def test_get_age_range(self):
        self.assertEqual((1, 13), get_age_range('b'))
        self.assertEqual((13, 26), get_age_range('y'))
        self.assertEqual((25, 38), get_age_range('a'))
        self.assertEqual((37, 97), get_age_range('s'))
        self.assertEqual((1, 97), get_age_range('b,s'))
        self.assertEqual((1, 38), get_age_range('b,a'))
        self.assertEqual((13, 97), get_age_range('y,s'))
        self.assertEqual((1, 26), get_age_range('b,y'))
        self.assertEqual((13, 38), get_age_range('y,a'))
        self.assertEqual((25, 97), get_age_range('a,s'))


class PugOrUghSerializersTest(Pregame, TestCase):
    '''Pug-or-Ugh serializers test.'''
    def test_contains_expected_fields(self):
        dog_serializer = DogSerializer(instance=self.dog1)
        user_serializer = UserSerializer(instance=self.user1)
        userpref_serializer = UserPrefSerializer(instance=self.userpref1)

        self.assertEqual(set(dog_serializer.data.keys()),
                         set(['id',
                              'name',
                              'image_filename',
                              'breed',
                              'age',
                              'gender',
                              'size',
                              'created_at']))
        self.assertEqual(set(userpref_serializer.data.keys()),
                         set(['user',
                              'age',
                              'gender',
                              'size',
                              'created_at',
                              'id']))
        self.assertEqual(set(user_serializer.data.keys()),
                         set(['last_login',
                              'is_active',
                              'username',
                              'first_name',
                              'last_name',
                              'email',
                              'is_staff',
                              'date_joined',
                              'is_superuser',
                              'groups',
                              'user_permissions',
                              'id']))

