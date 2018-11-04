from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    userBio = forms.CharField(widget=forms.Textarea(), max_length=1000)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'userBio', )


def poll_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'poll_topic/user_{0}/{1}'.format(instance.id, filename)
    
class CreatePoll(forms.Form):
    poll_title = forms.CharField(max_length=100)
    poll_op1 = forms.CharField(max_length=200)
    poll_op2 = forms.CharField(max_length=200)
    poll_op3 = forms.CharField(max_length=200)
    poll_op4 = forms.CharField(max_length=200)
    poll_op5 = forms.CharField(max_length=200)
    poll_op6 = forms.CharField(max_length=200)
    poll_op7 = forms.CharField(max_length=200)
    poll_op8 = forms.CharField(max_length=200)
    poll_op9 = forms.CharField(max_length=200)
    poll_op10 = forms.CharField(max_length=200)
    poll_op11 = forms.CharField(max_length=200)
    poll_op12 = forms.CharField(max_length=200)
    #poll_votes = forms.CharField(max_length=500)
    imgUrl = "static/avatar/man1.png"
    poll_img = forms.ImageField()

    def clean_poll_title(self):
        data = self.cleaned_data['poll_title']
        return data
    def clean_poll_options(self):
        data = self.cleaned_data['poll_options']
        return data
    def clean_poll_img(self):
        data = self.cleaned_data['poll_img']
        return data
