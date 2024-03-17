from django.db import models


class Post(models.Model):
    userId = models.IntegerField()
    title = models.CharField(max_length=256)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=60)
    publication_counter = models.IntegerField()
    rating = models.FloatField(null=True, default=1)