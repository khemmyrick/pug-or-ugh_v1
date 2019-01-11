from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.utils.translation import ugettext_lazy as _

from .signals import create_userpref, save_userpref


class PugorughConfig(AppConfig):
    name = 'pugorugh'

    def ready(self):
        post_save.connect(create_userpref, sender=User)
        post_save.connect(save_userpref, sender=User)
