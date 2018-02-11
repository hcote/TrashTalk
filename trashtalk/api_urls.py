from django.conf.urls import url

from accounts.views import UserListCreateView
from cleanups.views.api_views import (CleanupListCreateAPIView, CleanupDetailAPIView,
                                      LocationListCreateView)

urlpatterns = [
    url(r'^cleanups/$', CleanupListCreateAPIView.as_view(), name='cleanups'),
    url(r'^cleanups/(?P<pk>[0-9]+)/$', CleanupDetailAPIView.as_view(), name='cleanup-detail'),
    url(r'^locations/$', LocationListCreateView.as_view(), name='locations'),
    url(r'^users/$', UserListCreateView.as_view(), name='users'),
]
