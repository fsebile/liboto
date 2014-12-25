from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Media, Author, Publisher, Transaction, User
# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CustomUserAdmin, self).get_fieldsets(request, obj)
        if obj:
            fieldsets += (
                ("Liboto", {'fields': ('book_limit', 'favorite_medias')}),
            )
        return fieldsets

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