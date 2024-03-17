import requests
import environ
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Post

env = environ.Env()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'userId', 'title', 'body']
    list_filter = ['userId']
    search_fields = ['title']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('userId',)
        else:
            return self.readonly_fields

    def save_model(self, request, obj, form, change):
        response = requests.get('{env("EXTERNAL_API_URL")}/users/{obj.userId}')
        if response.status_code == 200:
            return super().save_model(request, obj, form, change)
        raise ValidationError('User with userId {obj.userId} not found')
