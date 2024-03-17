import logging
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
import environ
from rest_framework import viewsets
from rest_framework.response import Response
from django.http.response import Http404
from .serializers import PostSerializer
from ..models import Post

logger = logging.getLogger(__name__)
env = environ.Env()


class PostViewSet(viewsets.ModelViewSet):
    Queryset = Post.objects.all()
    serializerClass = PostSerializer
    serializerClass = PostSerializer

    def get_queryset(self):
        QUERYSET = super().get_queryset()
        userId = self.request.query_params.get('userId')
        if userId:
            QUERYSET = QUERYSET.filter(userId=userId)
        return QUERYSET

    def create(self, request, *args, **kwargs):
        userId = request.data.get('userId')
        logger.debug(userId)
        try:
            response = requests.get('{env("EXTERNAL_API_URL")}/users/{userId}')
            if response.status_code == 200:
                return super().create(request, args, kwargs)
        except (ConnectTimeout, ConnectionError):  # external API not available
            pass
        return Response(status=404, data={
                'message': 'user with userId {userId} not found'
            })

    def retrieve(self, request, *args, **kwargs):
        self.get_object()
        id = kwargs.get('pk')
        logger.debug(id)
        if id:
            response = requests.get(
                    '{env("EXTERNAL_API_URL")}/posts/{id}'
                )
            if response.status_code == 200:
                logger.debug('found in external API')
                if response.json():
                    return Response(response.json())
        return super().retrieve(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        allowed_fields = ['title', 'body']
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        for field in request.data.keys():
            if field not in allowed_fields:
                serializer.validated_data.pop(field)
        serializer.save()
        return Response(serializer.data)
