from django.forms import ModelForm, PasswordInput, CharField

from .models import User


class UserLoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    class Meta:
        model = User
        fields = ('username', 'password',)

    password = CharField(widget=PasswordInput)


class UserSignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password',)

    password_verification = PasswordInput()
