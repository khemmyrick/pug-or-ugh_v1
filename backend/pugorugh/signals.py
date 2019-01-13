from .models import UserPref


def create_userpref(sender, **kwargs):
    print('***SIGNAL WAS TRIGGERED***')
    if kwargs['created']:
        userpref = UserPref.objects.create(user=kwargs['instance'])


def save_userpref(sender, instance, **kwargs):
    print('***SIGNAL WAS TRIGGERED***')
    instance.profile.save()
