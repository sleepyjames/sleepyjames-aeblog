from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import logout_then_login 

from views import login, create_user

urlpatterns = patterns('',

    url(r'createuser/$', create_user, name="createuser"),

    url(r'login/$', login, name="login"),

    url(r'logout/$', logout_then_login, name="logout"),

)

