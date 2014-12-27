from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    book_limit = models.IntegerField(default=5)
    favorite_medias = models.ManyToManyField("Media", blank=True, null=True)

    @property
    def real_book_limit(self):
        return self.book_limit - self.transaction_set.filter(returned=False).count()

    @property
    def media_belonging(self):
        return self.transaction_set.filter(returned=False)

    @property
    def media_overdue(self):
        rlist = []
        for media_transaction in self.transaction_set.filter(returned=False):
            if media_transaction.is_past_due and not media_transaction.returned:
                rlist.append(media_transaction)
        return rlist


class Author(models.Model):
    name = models.CharField(max_length=160)

    def __unicode__(self):
        return u"{}".format(self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=160)

    def __unicode__(self):
        return u"{}".format(self.name)


class Media(models.Model):
    MEDIA_CHOICES = [
        ("b", "Book"),
        ("m", "Magazine"),
        ("n", "Newspaper"),
    ]

    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=320, default="-")
    year = models.CharField(max_length=4)
    publisher = models.ForeignKey(Publisher)
    author = models.ForeignKey(Author)
    cover_image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=MEDIA_CHOICES, default="b")
    total_stock = models.IntegerField(default=1)

    @property
    def type_verbose(self):
        return u"{}".format(dict(self.MEDIA_CHOICES)[self.type])

    def real_stock(self):
        return self.total_stock - self.transaction_set.filter(returned=False).count()
    real_stock.description = 'Real Stock'
    real_stock.allow_tags = True

    def __unicode__(self):
        return u"{}".format(self.title)


class Transaction(models.Model):
    media = models.ForeignKey(Media)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    cdate = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    duration = models.IntegerField(default=settings.LEND_DURATION)

    def clean(self):
        errors = {}
        if self.returned:
            return

        if self.media in self.user.media_belonging:
            errors.update({'media': ["User hasn't returned this {}.".format(self.media.type_verbose)]})

        if self.media.real_stock() < 1:
            errors.update({'media': ["This {} has no stock".format(self.type_verbose)]})

        if len(self.user.media_overdue):
            errors.update({'user': ["User has past due media."]})

        if self.user.real_book_limit < 1:
            errors.update({'user': ["User has no media limit left"]})

        raise ValidationError(errors)

    @property
    def is_past_due(self):
        return timezone.now() > self.cdate + timedelta(days=self.duration)

    @property
    def due_date(self):
        return self.cdate + timedelta(days=self.duration)

    def __unicode__(self):
        return u"{} - {}".format(self.media.title, self.user.username)