from discourz_app.models import Account
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from discourz.forms import SignUpForm


# Create your views here.
def profile(request):
    account = request.user.account

    context = {
        'username': account.user.username,
        'email': account.user.email,
        'bio' : account.bio,
        'img' : account.img,
    }

    return render(request, 'profile.html', context=context)

def registration(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            num_results = User.objects.filter(email = form.cleaned_data.get('email')).count()
            if num_results == 0:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.email = form.cleaned_data.get('email')
                user.account.img = form.cleaned_data.get('profile_img')
                user.account.bio = form.cleaned_data.get('userBio')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password, )
                login(request, user)
            else: 
                raise forms.ValidationError("This email address is in use.")
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})
    