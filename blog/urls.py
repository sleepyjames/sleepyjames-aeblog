from django.conf.urls.defaults import patterns, url, include

from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',

    url('^$', views.PostList.as_view(), name="post_list"),

    url('^archive/$', views.PostArchiveIndex.as_view(), name="post_archive"),

    url('^archive/(?P<year>(\d{2,4}))/$', views.PostArchive.as_view(), name="post_archive_year"),

    url('^archive/(?P<year>\d{2,4})/(?P<month>\d{1,2})/$', views.PostArchive.as_view(), name="post_archive_month"),

    url('^archive/(?P<year>\d{2,4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', views.PostArchive.as_view(), name="post_archive_day"),

    url('^post/view/(?P<slug>.*)/$', views.PostDetail.as_view(), name="post_detail"),

    url('^post/new/$', login_required(views.PostCreate.as_view()), name="post_create"),

    url('^post/(?P<pk>\d+)/edit/$', login_required(views.PostEdit.as_view()), name="post_edit"),

)
