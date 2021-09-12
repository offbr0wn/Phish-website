from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from signUp.models import Profile


# Takes default User model from django library and display's username and email field in profile page
class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', ]


# Uses Profile model in signup page for profile picture , where image field is shown
class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


# Delete user account  uses builtin User model
class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []  # Form has only submit button.  Empty "fields" list still necessary, though
