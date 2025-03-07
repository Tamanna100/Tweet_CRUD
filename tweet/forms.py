from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm
from .models import Tweet

class TweetForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ['text','photo'] #customized so field is list

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ('username','email','password1','password2') # buildin function so tuple; password 1 and 2 build in
	# names














