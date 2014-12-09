from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Media, Author, Publisher

# Create your views here.


class MediaListView(ListView):
    allow_empty = True
    http_method_names = [u'get']
    model = Media
    paginate_by = 3  # 25

    def get_queryset(self):
        isbn = self.request.GET.get("isbn", None)
        title = self.request.GET.get("title", None)
        year = self.request.GET.get("year", None)
        publisher = self.request.GET.get("publisher", None)
        author = self.request.GET.get("author", None)
        media_type = self.request.GET.get("type", None)

        query = {}

        if isbn is not None and len(isbn):
            query["isbn"] = isbn
        if title is not None and len(title):
            query["title__icontains"] = title
        if year is not None and len(year):
            query["year__year"] = year[:4]
        if publisher is not None and len(publisher):
            query["publisher__id"] = publisher
        if author is not None and len(author):
            query["author__id"] = author
        if media_type is not None and len(media_type):
            query["type"] = media_type

        return self.model.objects.filter(**query)


    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        context["authors"] = Author.objects.all().order_by("name")
        context["publishers"] = Publisher.objects.all().order_by("name")
        context["media_types"] = Media.MEDIA_CHOICES
        return context