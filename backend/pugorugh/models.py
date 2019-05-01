from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

GENDERS = (
    ('m', "male"),
    ('f', 'female'),
    ('u', 'unknown')
)
SIZES = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown')
)
STATUSES = (
    ('l', 'Liked'),
    ('d', 'disliked'),
    ('u', 'undecided')
)

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
    image_filename = models.CharField(max_length=500)
    breed = models.CharField(max_length=255,
                             default='Unknown Mix')
    age = models.IntegerField(default=1)
    gender = models.CharField(max_length=20,
                              choices=GENDERS,
                              default='u')
    size = models.CharField(max_length=20,
                            choices=SIZES,
                            default='s')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name+str(self.age)

    class Meta:
        ordering = ('-created_at',)


class UserPref(models.Model):
    '''
    A model representing user preferences.

    attrs:
        user: The user these preferences belong to.
        age: a str representing desired age range.
        gender: a str representing desired gender.
        size: a str representing desired size.
    '''
    user = models.ForeignKey(User, related_name='user_pref')
    age = models.CharField(max_length=20, default='b')
    gender = models.CharField(max_length=20, default='f')
    size = models.CharField(max_length=20, default='s')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-created_at',)

    @classmethod
    def create_default_pref(cls, user):
        cls.objects.create(user=user)


class UserDog(models.Model):
    """
    A model for storing a specific user's like/dislike of a dog.
    
    attrs:
        user: foreignkey user who has categorized a dog.
        dog: foreignkey dog object in question.
        status: str indicating that the user has liked or disliked the dog.
        created_at: time this object was created.
    """
    user = models.ForeignKey(User, related_name='user')
    dog = models.ForeignKey(Dog, related_name='users_dog')    
    status = models.CharField(max_length=20,
                              choices=STATUSES,
                              default='u')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "USER {} : DOG {}".format(self.user, self.dog)

    class Meta:
        ordering = ('-created_at',)
