from django.core.exceptions import ValidationError
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils import timezone
from . import views
from .models import Dog, UserDog, UserPref


# Create your tests here.
class Pregame(object):
    def setUp(self):
        """Setup function that can be repeated for all test cases.
        
        Creates sample Dog, UserDog, UserPref and User objects.
        Creates sample context dictionaries for certain Menu and Item objects.
        """
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
            'Joaquin Dean',
            'wahh@doublerdogs.com',
            'allofthebikes'
        )
        self.user2_russ = User.objects.create_user(
            'Russell Simmons',
            'bigdog@defjam.com',
            'kimorasex'
        )
        self.user3_dre = User.objects.create_user(
            'Andre Young',
            'billiondollarbeats@aftermath.com',
            'sixmilliondollarsman'
        )

        # Sample UserPrefs.
        self.userpref1_wahh = UserPref(
            user=self.user1_wahh,
            age='y',
            gender='m',
            size='m',
        )
        self.userpref2_russ = UserPref(
            user=self.user2_russ,
            age='a,s',
            gender='m',
            size='xl',
        )
        self.userpref3_dre = UserPref(
            user=self.user3_dre,
            age='b',
            gender='f',
            size='m',
        )

        # Sample UserDog Relationship Instances.
        self.userdog1_1 = UserDog(
            user=self.user1_wahh,
            dog=self.dog1_earl,
            status='l'
        )
        self.userdog2_1 = UserDog(
            user=self.user2_russ,
            dog=self.dog1_earl,
            status='l'
        )
        self.userdog3_1 = UserDog(
            user=self.user3_dre,
            dog=self.dog1_earl,
            status='d'
        )
        self.userdog1_2 = UserDog(
            user=self.user1_wahh,
            dog=self.dog2_eve,
            status='l'
        )
        self.userdog2_2 = UserDog(
            user=self.user2_russ,
            dog=self.dog2_eve,
            status='d'
        )
        self.userdog3_2 = UserDog(
            user=self.user3_dre,
            dog=self.dog2_eve,
            status='l'
        )
        self.userdog1_3 = UserDog(
            user=self.user1_wahh,
            dog=self.dog3_drag,
            status='l'
        )
        self.userdog2_3 = UserDog(
            user=self.user2_russ,
            dog=self.dog3_drag,
            status='d'
        )
        self.userdog3_3 = UserDog(
            user=self.user3_dre,
            dog=self.dog3_drag,
            status='l'
        )
        self.userdog1_4 = UserDog(
            user=self.user1_wahh,
            dog=self.dog4_jada,
            status='l'
        )
        self.userdog2_4 = UserDog(
            user=self.user2_russ,
            dog=self.dog4_jada,
            status='d'
        )
        self.userdog3_4 = UserDog(
            user=self.user3_dre,
            dog=self.dog4_jada,
            status='l'
        )
        self.userdog1_5 = UserDog(
            user=self.user1_wahh,
            dog=self.dog5_boom,
            status='l'
        )
        self.userdog2_5 = UserDog(
            user=self.user2_russ,
            dog=self.dog5_boom,
            status='d'
        )
        self.userdog3_5 = UserDog(
            user=self.user3_dre,
            dog=self.dog5_boom,
            status='l'
        )

class PugOrUghModelTests(Pregame, TestCase):
    '''Pug-or-ugh model tests.'''
    def test_dog_creation(self):
        '''A sample dog is created successfully.'''
        