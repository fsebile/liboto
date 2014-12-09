from django.contrib import admin
from .models import Media, Author, Publisher, Transaction
# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["media", "user", "cdate", "returned", "duration"]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["isbn", "title", "publisher", "author", "type",
                    "real_stock"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]