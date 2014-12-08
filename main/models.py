from django.db import models

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