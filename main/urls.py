from django.conf.urls import patterns, url
from .views import MediaListView, RequestMedia, Home

urlpatterns = patterns('',

    url(r'^list/media/', MediaListView.as_view(), name="media_list_url"),
    url(r'^/$', Home.as_view()),
    url(r'^request/media/$', RequestMedia.as_view(), name="request_media_url"),
)
