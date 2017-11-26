from django.conf.urls import url

from accounts.views import UserView
from cleanups.views import CleanupListCreateView, LocationView

urlpatterns = [
    url(r'^cleanups/', CleanupListCreateView.as_view(), name='cleanups'),
    url(r'^locations/', LocationView.as_view(), name='locations'),
    url(r'^users/', UserView.as_view(), name='users'),
]
