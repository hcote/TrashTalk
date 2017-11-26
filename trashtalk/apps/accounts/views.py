import logging

from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormMixin

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .forms import UserLoginForm, UserSignupForm
from .serializers import User, UserSerializer

log = logging.getLogger('accounts.views')


# pylint: disable=missing-docstring
class LoginView(GenericAPIView, FormMixin):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        log.info('Loading home view...')
        if request.user.is_authenticated():
            return Response({'user': request.user}, template_name=self.template_name)
        else:
            form = UserLoginForm()
            return Response({'form': form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        log.info('User logging in...')
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return Response({'user': user}, template_name=self.template_name)
        else:
            return Response({"error": "Login failed."},
                            status=status.HTTP_400_BAD_REQUEST)


# pylint: disable=missing-docstring
class SignupView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        # FIXME: Do some password checking, user validating, yada, yada
        form = UserSignupForm()
        return Response({'form': form}, template_name='signup.html')

    def post(self, request):
        # FIXME: Do some password checking, user validating, yada, yada
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return Response({'user': user}, template_name='index.html')


# pylint: disable=missing-docstring
class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer