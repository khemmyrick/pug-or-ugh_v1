from .models import UserPref


def create_userpref(sender, **kwargs):
    if kwargs['created']:
        userpref = UserPref.objects.create(user=kwargs['instance'])


def save_userpref(sender, instance, **kwargs):
    instance.profile.save()
