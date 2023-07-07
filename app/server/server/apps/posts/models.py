from django.db import models


class Post(models.Model):
    userId = models.IntegerField()
    title = models.CharField(max_length=256)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
