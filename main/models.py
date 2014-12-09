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


class Publisher(models.Model):
    name = models.CharField(max_length=160)


class Media(models.Model):
    isbn = models.BigIntegerField()
    title = models.CharField(max_length=160)
    year = models.DateField()
    publisher = models.ForeignKey(Publisher)
    author = models.ForeignKey(Author)
    cover_image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    stock = models.IntegerField(default=1)

    @property
    def real_stock(self):
        return self.stock - self.user_set.objects.count()

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
        all_not_returned = self.user.transaction_set.filter(returned=False)

        if (all_not_returned.filter(media=self.media).exists()
           and not self.returned):
            errors.update({'media': ["User hasn't returned this book."]})

        if (all_not_returned.count() > self.media.stock
           and not self.returned):
            errors.update({'media': ["This book has no stock"]})

        for media_transaction in all_not_returned:
            if media_transaction.is_past_due and not self.returned:
                errors.update({'user': ["User has past due media."]})

        raise ValidationError(errors)

    @property
    def is_past_due(self):
        return timezone.now() > self.cdate + timedelta(days=self.duration)
