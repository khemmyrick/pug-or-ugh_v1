from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView, UserPrefDetailView

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/user/preferences/$', UserPrefDetailView.as_view(), name='userpref')
])
'''
To get the next liked/disliked/undecided dog

/api/dog/<pk>/liked/next/
/api/dog/<pk>/disliked/next/
/api/dog/<pk>/undecided/next/
To change the dog's status

/api/dog/<pk>/liked/
/api/dog/<pk>/disliked/
/api/dog/<pk>/undecided/
To change or set user preferences

/api/user/preferences/
'''