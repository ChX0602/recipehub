from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^foodchaser/', include('foodchaser.urls')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^$', 'foodchaser.views.homepage'),
)
