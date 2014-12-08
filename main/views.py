from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Media, Author, Publisher

# Create your views here.


class MediaListView(ListView):
    allow_empty = True
    http_method_names = [u'get']
    model = Media
    paginate_by = 3  # 25