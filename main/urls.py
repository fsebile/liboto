from django.conf.urls import patterns, url
from .views import MediaListView, RequestMedia, Home, UserMedia, UserHome

urlpatterns = patterns('',
    url(r'^list/media/', MediaListView.as_view(), name="media_list_url"),
    url(r'^/$', Home.as_view()),
    url(r'^request/media/$', RequestMedia.as_view(), name="request_media_url"),
    url(r'^my/media/$', UserMedia.as_view(), name="user_media_url"),
    url(r'^my/home/$', UserHome.as_view(), name="user_home_url"),
)
