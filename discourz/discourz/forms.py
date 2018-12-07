from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
import re


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    userBio = forms.CharField(widget=forms.Textarea(), max_length=1000)
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['userBio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tell us about yourself'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'userBio', )
        widgets = {
            'userBio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Password'}),
            
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        }

class EditProfileForm(forms.Form):
    firstName = forms.CharField(max_length=50, required=False)
    lastName = forms.CharField(max_length=50, required=False)
    username = forms.CharField(max_length=50,required=False,disabled=True)
    email = forms.EmailField(required=False)
    profile_img = forms.ImageField(required=False)
    userBio = forms.CharField(widget=forms.Textarea(), max_length=1000, required=False)
    userTags = forms.CharField(widget=forms.Textarea(), max_length=1000, required=False)
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs.update({'class': 'form-control',})
        self.fields['lastName'].widget.attrs.update({'class': 'form-control',})
        self.fields['username'].widget.attrs.update({'class': 'form-control',})
        self.fields['profile_img'].widget.attrs.update({'style':'display:none;', 'id':'profile_img', 'onchange':"document.getElementById('blah').src = window.URL.createObjectURL(this.files[0])"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email'})        
        self.fields['userBio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tell us about yourself'})
        self.fields['userTags'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ex: #Travelling#Netflix,...'})
    
    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'username', 'email', 'userBio', )
        widgets = {
            'userBio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        }