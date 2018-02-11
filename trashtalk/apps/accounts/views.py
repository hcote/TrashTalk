import logging

from django.contrib.auth import authenticate, login
from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import User, UserSerializer

log = logging.getLogger('accounts.views')


def user_signup_view(request):
    return render(request, template_name='users/new.html')


# pylint: disable=missing-docstring
class LoginView(GenericAPIView):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        log.info('Loading home view...')
        if request.user.is_authenticated():
            return Response({'user': request.user}, template_name=self.template_name)
        else:
            return render(request, template_name='index.html')

    def post(self, request, *args, **kwargs):
        log.info('User logging in...')
        try:
            user = authenticate(request,
                                username=request.POST.get('username'),
                                password=request.POST.get('password'))
            login(request, user)
        except (AttributeError, Exception):
            log.exception("Login failed: %s", request.POST)
            return Response({"error": "Login failed."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user': user}, template_name=self.template_name)


# pylint: disable=missing-docstring
class UserDashboardView(RetrieveUpdateDestroyAPIView):
    """
    User can view and edit: profile, cleanups, and participation.
    Use formsets.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response({'user': request.user, 'cleanups': request.user.cleanups.all()},
                        template_name='users/detail.html')


# pylint: disable=missing-docstring
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer