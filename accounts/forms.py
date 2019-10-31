from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import UserProfile

class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta():
        model = User
        fields = ('first_name','last_name','username','password1', 'password2','email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfile
         fields = ('image','description', 'city')

class UserEditForm(forms.ModelForm):
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username',)
