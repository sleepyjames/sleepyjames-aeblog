from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import logout_then_login 

from django.contrib.auth.decorators import login_required
import views 


urlpatterns = patterns('',

    #url(r'^$', login_required(views.UserList.as_view()), 
    #    name="user_list"),

    #url(r'^user/(?P<pk>\d+)/$', 
    #    login_required(views.UserEdit.as_view()), 
    #    name="user_edit"),

    #url(r'createuser/$', views.create_user, name="createuser"),

    url(r'login/$', views.login, name="login"),

    url(r'logout/$', logout_then_login, name="logout"),

)

