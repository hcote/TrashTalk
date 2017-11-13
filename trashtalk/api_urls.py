from django.conf.urls import url
from cleanups.views import CleanupViews, LocationViews

urlpatterns = [
    url(r'^cleanups/', CleanupViews.as_view(), name='cleanups'),
    url(r'^locations/', LocationViews.as_view(), name='locations'),
]
