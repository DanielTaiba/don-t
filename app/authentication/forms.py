from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
  password1 = forms.CharField(
    max_length=63, 
    widget=forms.PasswordInput(attrs={
      'class':"form-control", 
      'id':"floatingPassword",
      'placeholder':"Password"
      }),
    label='Password'
  )
  password2 = forms.CharField(
    max_length=63, 
    widget=forms.PasswordInput(attrs={
      'class':"form-control", 
      'id':"floatingPassword",
      'placeholder':"Repeat Password"
      }),
    label='Repeat Password'
  )

  class Meta:
    model = CustomUser
    fields = ('email',)
    label = {
      'email':'Email',
    }
    
    widgets = {
      'email': forms.EmailInput(attrs={
        'class':"form-control", 
        'id':"floatingInput",
        'placeholder':"name@example.com"}),
    }


class CustomUserChangeForm(UserChangeForm):

  class Meta:
    model = CustomUser
    fields = ('email',)

class LoginForm(forms.Form):
  email = forms.EmailField(
    label='Email',
    widget=forms.EmailInput(attrs={
      'class':"form-control", 
      'id':"floatingInput",
      'placeholder':"name@example.com"})
  )
  password = forms.CharField(
    max_length=63, 
    widget=forms.PasswordInput(attrs={
      'class':"form-control", 
      'id':"floatingPassword",
      'placeholder':"Password"
      }),
    label='Contraseña'
  )