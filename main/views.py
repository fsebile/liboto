from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import Media, Author, Publisher

# Create your views here.


class MediaListView(ListView):
    allow_empty = True
    http_method_names = [u'get']
    model = Media
    paginate_by = 3  # 25

    @staticmethod
    def get_search_parameters(request, search_params, query_params=None):
        if query_params is None:
            query_params = {}

        qdict = {}

        for param in search_params:
            val = request.GET.get(param, None)
            if val is not None and len(val):
                qdict[query_params.get(param, param)] = val

        return qdict

    def get_queryset(self):
        query = self.get_search_parameters(
            request=self.request,
            search_params=["isbn", "title", "year",
                           "publisher", "author", "type"],
            query_params={"isbn": "isbn__icontains",
                          "title": "title__icontains",
                          "year": "year__year",
                          "publisher": "publisher__id",
                          "author": "author__id"})
        return self.model.objects.filter(**query)

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        context["authors"] = Author.objects.all().order_by("name")
        context["publishers"] = Publisher.objects.all().order_by("name")
        context["media_types"] = Media.MEDIA_CHOICES
        return context


class Home(TemplateView):
    template_name = "main/home.html"
