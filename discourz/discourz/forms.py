from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    profile_img = forms.ImageField()
    userBio = forms.CharField(widget=forms.Textarea(), max_length=1000)

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_img', 'password1', 'password2', 'userBio', )