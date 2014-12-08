from django.contrib import admin
from .models import Media, Author, Publisher
# Register your models here.


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass