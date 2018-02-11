"""trashtalk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings

from accounts.views import (LoginView, UserDashboardView, user_signup_view)
from cleanups.views.template_views import (cleanup_new, cleanup_edit, cleanup_list,
                                           cleanup_show, cleanup_create, cleanup_update,
                                           cleanup_join_view)

urlpatterns = [
    # Homepage
    url(r'^$', LoginView.as_view(), name='home'),

    # Admin Pages
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api/v1/', include('api_urls', namespace='api')),

    # Auth
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/', user_signup_view, name='register'),

    # User
    # TODO: Issue #83 - Move to accounts/urls.py
    url(r'^dashboard/', UserDashboardView.as_view(), name='dashboard'),

    # Cleanups
    # TODO: Issue #83 - Move to cleanups/urls.py
    url(r'^cleanups/$', cleanup_list, name='cleanups-list'),
    url(r'^cleanups/new/$', cleanup_new, name='cleanup-new'),
    url(r'^cleanups/create/$', cleanup_create, name='cleanup-create'),
    url(r'^cleanups/(?P<pk>[0-9]+)/edit/$', cleanup_edit, name='cleanup-edit'),
    url(r'^cleanups/(?P<pk>[0-9]+)/update/$', cleanup_update, name='cleanup-update'),
    url(r'^cleanups/(?P<pk>[0-9]+)/join/$', cleanup_join_view, name='join-cleanup'),
    url(r'^cleanups/(?P<pk>[0-9]+)/$', cleanup_show, name='cleanup-detail'),

    # Development Only
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += [url(r'^docs/', include('rest_framework_docs.urls'))]
