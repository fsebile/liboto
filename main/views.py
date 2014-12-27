from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.base import TemplateView, View
from django.utils import timezone

from .models import Media, Transaction


class MediaListView(ListView):
    allow_empty = True
    http_method_names = [u'get']
    model = Media
    paginate_by = 10

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
                          "year": "year__icontains",
                          "publisher": "publisher__name__icontains",
                          "author": "author__name__icontains"})
        return self.model.objects.filter(**query)

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        context["media_types"] = Media.MEDIA_CHOICES
        return context


class Home(TemplateView):
    template_name = "main/home.html"

class UserHome(TemplateView):
    template_name = "main/user_home.html"


class UserMedia(TemplateView):
    template_name = "main/user_media.html"

    def get_context_data(self, **kwargs):
        context = super(UserMedia, self).get_context_data(**kwargs)
        context["transactions"] = self.request.user.transaction_set.order_by("returned", "cdate")
        context["now"] = timezone.now()
        return context


class UserFavorites(TemplateView):
    template_name = "main/user_favorites.html"

    def get_context_data(self, **kwargs):
        context = super(UserFavorites, self).get_context_data(**kwargs)
        context["favorites"] = self.request.user.favorite_medias.all()
        return context


class FavoriteMedia(View):
    http_method_names = ["get", "post"]

    def post(self, request, *args, **kwargs):
        if {"media_id", "method"} <= set(request.POST.keys()):
            media_q = Media.objects.filter(pk=request.POST["media_id"])
            if media_q.exists():
                if request.POST["method"] == "add":
                    request.user.favorite_medias.add(media_q.first())
                    messages.add_message(request, messages.INFO,
                                         "Media added to your favorites.")
                    return HttpResponseRedirect(redirect_to=reverse("media_list_url"))
                elif request.POST["method"] == "remove":
                    request.user.favorite_medias.remove(media_q.first())
                    messages.add_message(request, messages.INFO,
                                         "Media removed from your favorites.")
                    return HttpResponseRedirect(redirect_to=reverse("user_favorites_url"))

        messages.add_message(request, messages.WARNING,
                             "An error occured, please inform us.")
        return HttpResponseRedirect(redirect_to=reverse("media_list_url"))

    def get(self, request, *args, **kwargs):  # get is forbidden
        messages.add_message(request, messages.WARNING,
                             "You've tried to access a forbidden page.")
        return HttpResponseRedirect(redirect_to=reverse("home"))


class RequestMedia(TemplateView):
    template_name = "main/request_media.html"
    http_method_names = ["get", "post"]

    def post(self, request, *args, **kwargs):
        if "choice" in request.POST.keys():
            choice = request.POST["choice"]
            if choice == u"true" and "media_id" in request.POST.keys():
                media = Media.objects.filter(pk=request.POST["media_id"])
                if media.exists():
                    if media.first().real_stock() < 1:
                        messages.add_message(request, messages.WARNING,
                                         "Requested media does not have stock.")
                    else:
                        t = Transaction(
                            media=media.first(),
                            user=request.user)
                        try:
                            t.full_clean()
                            t.save()
                            messages.add_message(request, messages.SUCCESS,
                                             "Your request is reserved.")
                        except ValidationError as e:
                            for field in e.message_dict.values():
                                for error in field:
                                    messages.add_message(request,
                                                         messages.ERROR,
                                                         error)
                else:
                    messages.add_message(request, messages.WARNING,
                                     "Media does not exist.")

            elif choice == u"false":
                messages.add_message(request, messages.INFO,
                                     "Cancelled reservation.")
            else:
                messages.add_message(request, messages.WARNING,
                                     "Invalid request.")
            return HttpResponseRedirect(redirect_to=reverse("media_list_url"))
        else:
            try:
                context = self.get_context_data(**kwargs)
                return self.render_to_response(context)
            except IndexError as e:
                messages.add_message(request, messages.WARNING, e.message)
                return HttpResponseRedirect(redirect_to=reverse("home"))

    def get(self, request, *args, **kwargs):  # get is forbidden
        messages.add_message(request, messages.WARNING,
                             "You've tried to access a forbidden page.")
        return HttpResponseRedirect(redirect_to=reverse("home"))

    def get_context_data(self, **kwargs):
        context = super(RequestMedia, self).get_context_data(**kwargs)
        media_id = self.request.POST.get("media_id", None)
        if media_id is not None and len(media_id):
            media = Media.objects.filter(pk=media_id)
            if media.exists():
                context["media"] = media.first()
                return context
            else:
                raise IndexError("Media does not exist.")
        else:
            raise IndexError("Invalid Access.")
