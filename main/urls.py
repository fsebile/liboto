from django.conf.urls import patterns, url
from .views import MediaListView

urlpatterns = patterns('',

    url(r'^list/media/', MediaListView.as_view(), name="media_list_url"),
)
