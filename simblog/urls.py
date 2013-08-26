from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from blog import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simblog.views.home', name='home'),
    # url(r'^simblog/', include('simblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'^complete/$', views.complete, name='complete'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'', include('social_auth.urls')),
)
