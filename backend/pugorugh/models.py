from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Dog(models.Model):
    '''
    A model representing dogs on the site.
    
    attrs:
        name: a str
        image_filename: a str
        breed: a str
        gender, a str: “m” for male, “f” for female, “u” for unknown
        size, a str: "s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown
    '''
    name = models.CharField(max_length=255)
    image_filename = models.CharField(default='', max_length=500)
    breed = models.CharField(default='Unknown Mix', max_length=255)
    age = models.IntegerField(default=1)
    gender = models.CharField(default='f', max_length=3)
    size = models.CharField(default='s', max_length=3)

    def __str__(self):
        return self.name


class UserPref(models.Model):
    '''
    A model representing user preferences.

    attrs:
        user: The user these preferences belong to.
        age: a str representing desired age range.
        gender: a str representing desired gender.
        size: a str representing desired size.
    '''
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    # ForeignKey didnt ring any error bells...
    # models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.CharField(default='b', max_length=3)
    gender = models.CharField(default='f', max_length=3)
    size = models.CharField(default='s', max_length=3)
    age_key = {
        'b': 'baby',
        'y': 'young',
        'a': 'adult',
        's': 'senior'
    }
    gender_key = {
        'm': 'male',
        'f': 'female'
    }
    size_key = {
        's': 'small',
        'm': 'medium',
        'l': 'large',
        'xl': 'extra-large'
    }

    def __str__(self):
        return '{} prefers a {}, {}, {} dog.'.format(
            self.user,
            str(self.age_key[self.age]),
            self.size_key[self.size],
            self.gender_key[self.gender]
        )



class UserDog(models.Model):
    '''
    A model indicating a user's affinity for a specific dog.
    
    If user or dog object are deleted, the relationship instance deletes too.
    '''
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
    )
    dog = models.OneToOneField(
        'dog',
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=3)

    class Meta:
        unique_together = ['user', 'dog']
        # Each user may only "swype" on a dog once.

    def __str__(self):
        if self.status == 'l':
            return 'You liked {}.'.format(self.dog.name)
        elif self.status == 'd':
            return 'You disliked {}.'.format(self.dog.name)
        return "You haven't decided on {}.".format(self.dog.name)


## function to create userpref when a user is registered.
def create_userpref(sender, **kwargs):
    if kwargs['created']:
        userpref = UserPref.objects.create(user=kwargs['instance'])


post_save.connect(create_userpref, sender=User)
