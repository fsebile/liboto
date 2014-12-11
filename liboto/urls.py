from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import Home as main_home

urlpatterns = patterns('',
    # Examples:
    url(r'^$', main_home.as_view(), name='home'),
    url(r'^automaton/', include('main.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
)
