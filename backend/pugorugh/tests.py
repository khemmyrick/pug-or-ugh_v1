from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils import timezone
## from django_downloadview import setup_view
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
from . import views
from .models import Dog, UserDog, UserPref
from .utils import get_age_range


# Create your tests here.
class Pregame(object):
    def setUp(self):
        """Setup function that can be repeated for all test cases.
        
        Creates sample Dog, UserDog, UserPref and User objects.
        Creates sample context dictionaries for certain Menu and Item objects.
        """
        # Request factory.
        self.factory = APIRequestFactory()

        # Sample Dogs.
        self.dog1_earl = Dog(
            name='Earl',
            image_filename='earl.png',
            breed='werewolf',
            age=84,
            gender='m',
            size='xl',
        )
        self.dog1_earl.save()
        self.dog2_eve = Dog(
            name='Eve',
            image_filename='eve.png',
            breed='pit bull',
            age=72,
            gender='f',
            size='l',
        )
        self.dog2_eve.save()
        self.dog3_drag = Dog(
            name='Dragon',
            image_filename='dragon.png',
            breed='chiwawa',
            age=70,
            gender='m',
            size='s',
        )
        self.dog3_drag.save()
        self.dog4_jada = Dog(
            name='Jada',
            image_filename='jada.png',
            breed='terrier',
            age=82,
            gender='u',
            size='m',
        )
        self.dog4_jada.save()
        self.dog5_boom = Dog(
            name='Boomer',
            image_filename='boomer.png',
            breed='alpha dog',
            age=1,
            gender='u',
            size='u',
        )
        self.dog5_boom.save()

        ## Sample Users.
        self.user1_wahh = User.objects.create_user(
            'Joaquin',
            'wahh@doublerdogs.com',
            'allofthebikes'
        )
        self.user1_wahh.save()
        self.user2_russ = User.objects.create_user(
            'Russell',
            'bigdog@defjam.com',
            'kimorasex'
        )
        self.user2_russ.save()
        self.user3_dre = User.objects.create_user(
            'Andre',
            'billiondollarbeats@aftermath.com',
            'sixmilliondollarsman'
        )
        self.user3_dre.save()

        # Sample UserPrefs.
        self.userpref1_wahh = UserPref(
            user=self.user1_wahh,
            age='y',
            gender='m',
            size='m',
        )
        self.userpref1_wahh.save()
        self.userpref2_russ = UserPref(
            user=self.user2_russ,
            age='a,s',
            gender='m',
            size='xl',
        )
        self.userpref2_russ.save()
        self.userpref3_dre = UserPref(
            user=self.user3_dre,
            age='b',
            gender='f',
            size='m',
        )
        self.userpref3_dre.save()

        # Sample UserDog Relationship Instances.
        self.userdog1 = UserDog(
            user=self.user1_wahh,
            dog=self.dog2_eve,
            status='l'
        )
        self.userdog1.save()
        self.userdog2 = UserDog(
            user=self.user2_russ,
            dog=self.dog1_earl,
            status='l'
        )
        self.userdog2.save()
        self.userdog3 = UserDog(
            user=self.user3_dre,
            dog=self.dog2_eve,
            status='d'
        )
        self.userdog3.save()


class PugOrUghModelTests(Pregame, TestCase):
    '''Pug-or-ugh model tests.'''
    def test_dog_creation(self):
        '''A sample dog is created successfully.'''
        self.assertEqual(self.dog1_earl.name, 'Earl')
        self.assertNotEqual(self.dog1_earl.gender, self.dog2_eve.gender)
        self.assertLessEqual(self.dog3_drag.created_at, timezone.now())
        
    def test_user_pref_creation(self):
        '''A sample user preferences profile is created successfully.'''
        self.assertEqual(self.userpref1_wahh.user, self.user1_wahh)
        self.assertNotEqual(self.userpref2_russ.user, self.user3_dre)
        self.assertLessEqual(self.userpref3_dre.created_at, timezone.now())
        
    def test_user_dog_creation(self):
        '''A sample relationship object is created for a user and dog.'''
        self.assertEqual(self.userdog1.status, 'l')
        self.assertNotEqual(self.userdog2.dog, self.dog2_eve)
        self.assertLessEqual(self.userdog2.created_at, timezone.now())


class PugOrUghViewTests(Pregame, TestCase):
    '''Pug-or-ugh view tests.'''
    def test_user_register_view(self):
        resp = self.client.post(
            '/api/user/', 
            {'username': 'andre',
             'password': 'sixmilliondollarsman'}
        )
        user_pref = UserPref.objects.get(user=self.user3_dre)
        self.assertEqual(resp.status_code, 201)
        self.assertNotEqual(user_pref, None)

    def test_retrieve_update_user_pref_view(self):
        view = views.RetrieveUpdateUserPrefView.as_view()
        user = self.user3_dre
        data = {'id': user.id,
                'age': 's',
                'gender': self.dog1_earl.gender,
                'size': self.dog1_earl.size}
        request = self.factory.put('/api/user/preferences/', data=data)
        force_authenticate(request, user=user)
        resp = view(request)
        self.assertNotEqual(resp.status_code, 401)
        self.assertEqual(resp.status_code, 200)

    def test_retrieve_update_user_pref_view_unauth(self):
        view = views.RetrieveUpdateUserPrefView.as_view()
        user = self.user3_dre
        data = {'id': user.id,
                'age': 's',
                'gender': self.dog1_earl.gender,
                'size': self.dog1_earl.size}
        request = self.factory.put('/api/user/preferences/', data=data)
        resp = view(request)
        self.assertEqual(resp.status_code, 401)

    def test_user_dog_liked_view(self):
        view = views.UserDogLikedView.as_view()
        user = self.user3_dre
        # token, is_created = Token.objects.get_or_create(user=user)
        # data = {'id': user.id,
        #        'token': token,
        #        }
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '-1'}))
        force_authenticate(request, user=user)
        resp = view(request)
        self.assertEqual(resp.status_code, 404)
        request = self.factory.put(reverse('dog-liked', kwargs={'pk': '3'}))
        force_authenticate(request, user=user)
        resp = view(request)
        self.assertEqual(resp.status_code, 201)
        # dog = self.dog2_eve
        # data = 
        # request = self.factory.put(
        #    '/api/dog/{}/liked/'.format(dog.pk),
        #    dog=dog,
        #    defaults={'user': user,
        #              'dog': dog,
        #              'status': 'l'}
        # )
        # force_authenticate(request, user=user)
        # resp = view(request)
        # self.assertEqual(resp.status_code, 200)



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