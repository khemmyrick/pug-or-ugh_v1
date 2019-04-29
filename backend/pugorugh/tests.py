from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils import timezone
## from django_downloadview import setup_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 APIClient, force_authenticate)
from . import views
from .models import Dog, UserDog, UserPref
from .utils import get_age_range
from .serializers import DogSerializer, UserSerializer, UserPrefSerializer


USER_DATA = {'username': 'test_user',
             'email': 'test@example.com',
             'password': 'p4ssw0rd'}


# Create your tests here.
class CustomPugorUghTestMixin(object):
    def setUp(self):
        # self.factory = APIRequestFactory()
        self.user0 = User.objects.create_user(
            username='test_user',
            email='test@example.com', # Same data as USER_DATA
            password='p4ssw0rd'
        )
        self.user0.save()
        
        auth = self.client.post('/api-token-auth/', USER_DATA)
        token = auth.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class Pregame(object):
    # @classmethod
    # def setUpClass(cls):
    #    super().setUpClass()
    #    cls.api_client = APIClient()
    #    # user0 = User.objects.create_user(
    #    #    username='test_user',
    #    #    email='test@example.com', # Same data as USER_DATA
    #    #    password='p4ssw0rd'
    #    # )
    #    # user0.save()
    # @classmethod
    # def tearDownClass(cls):
    #    super().tearDownClass()
    #    cls.api_client = None
    #    # u = User.objects.get(username='test_user')
    #    # u.delete()
    def setUp(self):
        """Setup function that can be repeated for all test cases.
        
        Creates sample Dog, UserDog, UserPref and User objects.
        Creates sample context dictionaries for certain Menu and Item objects.
        """
		# USER_DATA is a Dict holding my test user username/password
        # auth = self.api_client.post('/api-token-auth/', USER_DATA)
        # token = auth.data['token']
        # Use Token Auth for APIClient for each def test_
        # self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Request factory.
        self.factory = APIRequestFactory()
        self.api_client = APIClient()

        # Sample Dogs.
        self.dog1 = Dog(
            name='Dog1',
            image_filename='dog1.png',
            breed='dog1',
            age=2,
            gender='m',
            size='xl',
        )
        self.dog1.save()
        self.dog2 = Dog(
            name='Dog2',
            image_filename='dog2.png',
            breed='dog2',
            age=36,
            gender='f',
            size='l',
        )
        self.dog2.save()
        self.dog3 = Dog(
            name='Dog3',
            image_filename='dog3.png',
            breed='dog3',
            age=96,
            gender='m',
            size='s',
        )
        self.dog3.save()

        # Sample Users.
        # User0 must exist BEFORE client can "login" as user0.
        # self.user0 = User.objects.create_user(
        #    username='test_user',
        #    email='test@example.com', # Same data as USER_DATA
        #    password='p4ssw0rd'
        # )
        # self.user0.save()
        self.user1 = User.objects.create_user(
            'User1',
            'user1@example.com',
            'allofthebikes'
        )
        self.user1.save()
        self.user2 = User.objects.create_user(
            'User2',
            'user2@example.com',
            'kimorasex'
        )
        self.user2.save()
        self.user3 = User.objects.create_user(
            'User3',
            'user3@example.com',
            'sixmilliondollarsman'
        )
        self.user3.save()

        # Sample UserPrefs.
        self.userpref1 = UserPref(
            user=self.user1,
            age='y',
            gender='m',
            size='m',
        )
        self.userpref1.save()
        self.userpref2 = UserPref(
            user=self.user2,
            age='a,s',
            gender='f',
            size='l',
        )
        self.userpref2.save()
        self.userpref3 = UserPref(
            user=self.user3,
            age='b',
            gender='f',
            size='m',
        )
        self.userpref3.save()

        # Sample UserDog Relationship Instances.
        self.userdog1 = UserDog(
            user=self.user1,
            dog=self.dog2,
            status='l'
        )
        self.userdog1.save()
        self.userdog2 = UserDog(
            user=self.user2,
            dog=self.dog1,
            status='l'
        )
        self.userdog2.save()
        self.userdog3 = UserDog(
            user=self.user3,
            dog=self.dog2,
            status='d'
        )
        self.userdog3.save()
        
        self.dog_serializer = DogSerializer(instance=self.dog1)
        self.user_serializer = UserSerializer(instance=self.user1)
        self.userpref_serializer = UserPrefSerializer(instance=self.userpref1)


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


class UserRegTests(CustomPugorUghTestMixin, APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        New UserPref object is simultaneously created.
        """
        
        # auth = self.client.post('/api-token-auth/', USER_DATA)
        # token = auth.data['token']
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # new_data will provide blueprint for new_user.
        new_data = {'username': 'new_user',
                    'email': 'newuser@example.com',
                    'password': 'bendtheKnee806GoT'}
                    
        # url gets us to view being tested.
        url = reverse('register-user')
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        # setUp user0 plus new_user == 2
        # check user via username.  email and/or password may not be available for testing suite?
        self.assertEqual(User.objects.get(username='new_user').username,
                         'new_user')
        user_pref = UserPref.objects.get(user=User.objects.get(username='new_user'))
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
        # UserDog in question SHOULD have status of 'l' after view is accessed.

    def test_user_dog_disliked_view(self):
        '''
        Test UserDogDislikedView
        '''
        view = views.UserDogDislikedView.as_view()
        user = self.user3
        dog = self.dog2
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '3'}))
        # request = self.api_client.put('/api/dog/3/liked', kwargs={'pk': '3'})
        # What do I need to send with this request?
        force_authenticate(request, user=user)
        resp = view(request, pk='3')
        # This response is HTML, not json.
        self.assertEqual(resp.status_code, 200)


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
        data_dog = self.dog_serializer.data
        data_user = self.user_serializer.data
        data_userpref = self.userpref_serializer.data
        self.assertEqual(set(data_dog.keys()), set(['id',
                                                    'name',
                                                    'image_filename',
                                                    'breed',
                                                    'age',
                                                    'gender',
                                                    'size',
                                                    'created_at']))
        self.assertEqual(set(data_userpref.keys()), set(['user',
                                                     'age',
                                                     'gender',
                                                     'size',
                                                     'created_at',
                                                     'id']))
        self.assertEqual(set(data_user.keys()), set(['last_login',
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

