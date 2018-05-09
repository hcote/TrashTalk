import logging
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.parsers import FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import User, UserSerializer

from cleanups.models import Cleanup

log = logging.getLogger('accounts.views')


def user_signup_view(request):
    return render(request, template_name='users/new.html')


def user_signup_create(request):
    log.info("Signup submitted ...")
    invalid = any([request.POST.get('password') != request.POST.get('confirm_password')])
    if invalid:
        log.info('User passwords do not match.')
        return redirect('register')
    try:
        user = User.objects.create_user(request.POST.get('username'),
                                        request.POST.get('email'),
                                        request.POST.get('password'))
        login(request, user)
    except (AttributeError, IntegrityError):
        log.exception('Error while creating a new user.')
        return redirect('register')
    else:
        log.info("Signup successful.")
        return redirect('home')


# pylint: disable=missing-docstring
class LoginView(GenericAPIView):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser,]
    permission_classes = (AllowAny,)
    template_name = 'index.html'

    def get(self, request):
        log.info('Loading home view...')
        if request.user.is_authenticated:
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
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'user': request.user,
                         'cleanups': request.user.cleanups.all(),
                         'cleanups_joined': self.get_cleanup_participation(request.user)},
                        template_name='users/detail.html')

    @staticmethod
    def get_cleanup_participation(user):
        current_cleanups = Cleanup.objects.filter(date__gte=datetime.today())
        return [event for event in current_cleanups if user in event.participants.all()]


# pylint: disable=missing-docstring
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser,)


# pylint: disable=missing-docstring
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


# pylint: disable=missing-docstring
class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
