import unicodedata
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "auto-capitalize": "none",
            "autocomplete": "username",
        }


class UserLoginForm(AuthenticationForm):

    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": "This account is inactive.",
    }


class EditUserForm(forms.ModelForm):
    class Meta:
        models: User
        exclude = ['email', 'username']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['username']

    widgets = {
        "bio": forms.TextInput(attrs={'class': 'form-control'}),
        "image": forms.ImageField(attrs={'class': 'form-control', }),
        "is_active": forms.HiddenInput(),
    }
    labels = {
        "bio": "بیو",
        "image": "عکس",
    }


