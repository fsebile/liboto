from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

# Create your models here.
MEDIA_CHOICES = [
    ("b", "Book"),
    ("m", "Magazine"),
    ("n", "Newspaper"),
]


class Author(models.Model):
    name = models.CharField(max_length=160)

    def __unicode__(self):
        return u"{}".format(self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=160)

    def __unicode__(self):
        return u"{}".format(self.name)


class Media(models.Model):
    isbn = models.BigIntegerField()
    title = models.CharField(max_length=160)
    year = models.DateField()
    publisher = models.ForeignKey(Publisher)
    author = models.ForeignKey(Author)
    cover_image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    total_stock = models.IntegerField(default=1)

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
        users_books = self.user.transaction_set.filter(returned=False)

        if (users_books.filter(media=self.media).exists()
           and not self.returned):
            errors.update({'media': ["User hasn't returned this book."]})

        if self.media.real_stock() < 1 and not self.returned:
            errors.update({'media': ["This book has no stock"]})

        for media_transaction in users_books:
            if media_transaction.is_past_due and not self.returned:
                errors.update({'user': ["User has past due media."]})

        raise ValidationError(errors)

    @property
    def is_past_due(self):
        return timezone.now() > self.cdate + timedelta(days=self.duration)

    def __unicode__(self):
        return u"{} - {}".format(self.media.title, self.user.username)