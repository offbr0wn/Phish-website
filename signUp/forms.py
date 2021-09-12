
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Using user form from django library as template , is passed through CreateUserForm with form details,
# where is passed into the views of the sign up page
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True) # Email field must be valid in order to create user
    #
    class Meta:
        model = User
        # The fields is what is displayed when user signs up a, takes the information within the html template
        fields = ['username', 'email', 'password1', 'password2']

