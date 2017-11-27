from django.conf.urls import url

from accounts.views import UserAPIView
from cleanups.views import CleanupListCreateView, LocationListCreateView

urlpatterns = [
    url(r'^cleanups/', CleanupListCreateView.as_view(), name='cleanups'),
    url(r'^locations/', LocationListCreateView.as_view(), name='locations'),
    url(r'^users/', UserAPIView.as_view(), name='users'),
]
