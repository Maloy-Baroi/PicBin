from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'first_name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'last_name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)


class EditUserProfile(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = UserProfile
        exclude = ('user', )
