from django.conf.urls.defaults import patterns, url, include

from django.contrib.auth.views import login, logout_then_login

from django.views.generic import TemplateView

urlpatterns = patterns('',

    (r'^accounts/', include('auth.urls')),

    url(r'^$', TemplateView.as_view(template_name="index.html"), name="home"),

)
