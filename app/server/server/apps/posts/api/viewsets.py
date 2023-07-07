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
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        userId = self.request.query_params.get('userId')
        if userId:
            queryset = queryset.filter(userId=userId)
        return queryset

    def create(self, request, *args, **kwargs):
        userId = request.data.get('userId')
        logger.debug(userId)
        try:
            response = requests.get(f'{env("EXTERNAL_API_URL")}/users/{userId}')
            if response.status_code == 200:
                return super().create(request, args, kwargs)
        except (ConnectTimeout, ConnectionError):  # external API not available
            pass
        return Response(status=404, data={
                'message': f'user with userId {userId} not found'
            })

    def retrieve(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Http404:
            id = kwargs.get('pk')
            logger.debug(id)
            if id:
                try:
                    response = requests.get(
                            f'{env("EXTERNAL_API_URL")}/posts/{id}'
                        )
                    if response.status_code == 200:
                        logger.debug('found in external API')
                        if response.json():
                            return Response(response.json())
                except (ConnectionError, ConnectTimeout):  # external API not available
                    pass
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
