from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
from .apps.posts.api import router
from .apps.posts.views import api_docs

urlpatterns = [ 
    path("", RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path('', include('django_prometheus.urls')),
    path("api/docs/", api_docs, name='api_docs'),
    path("baton/", include('baton.urls')),
]
