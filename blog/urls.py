from django.conf.urls import patterns, include, url

from blog import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
    url(r'^posts/(?P<year>\w+)/$', views.posts, name='posts_all'),
    url(r'^posts/(?P<year>\d{4})/$', views.posts, name='posts_by_year'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1})/$', views.posts_by_month, name='posts_by_month'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{2})/$', views.posts_by_month, name='posts_by_month'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{2})/$', views.posts_by_day, name='posts_by_day'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1})/(?P<day>\d{1})/$', views.posts_by_day, name='posts_by_day'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.posts_by_day, name='posts_by_day'),
    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1})/$', views.posts_by_day, name='posts_by_day'),
    url(r'^posts/tag/(?P<tag>\w+)/$', views.posts_by_tag, name='posts_by_tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
)
