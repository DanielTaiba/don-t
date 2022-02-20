from django.shortcuts import redirect, render
from django.contrib import messages
from authentication.models import CustomUser
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def welcome(request):
  return render(request,'welcome.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

class loginPage(View):
  template_name = 'auth/login.html'
  form_class = LoginForm

  def get(self,request):
    if request.user.is_authenticated:
        return redirect("welcome")
    else:
      form = self.form_class()
      message = 'login'
      context = {
        'form':form,
        'msg' : message
      }
      return render(request,self.template_name,context = context)
  
  def post (self,request):
    form = self.form_class(request.POST)
    if form.is_valid():
      user = authenticate(
        email = form.cleaned_data['email'],
        password  = form.cleaned_data['password']
      )
      if user is not None:
        login(request,user)
        return redirect('welcome')
      else:
        messages.info(request, 'Nombre de usuario o contraseña esta incorrecta')

    context = {
      'form': form,
      'msg':'login failed'
    }
    return render(request,self.template_name,context = context)


class signUpPage(View):
  template_name = 'auth/sign-up.html'
  form_class = CustomUserCreationForm

  def get(self,request):
    if request.user.is_authenticated:
      logout(request)
      return redirect('sign-up')
    else:
      form = self.form_class()
      message = 'signin'
      context = {
        'form':form,
        'msg' : message
      }
      return render(request,self.template_name,context = context)
  
  def post (self,request):
    form = self.form_class(request.POST)
    if form.is_valid():
      if form.cleaned_data['password1'] == form.cleaned_data['password2'] and form.cleaned_data['password1'] is not None:
        user = CustomUser.objects.create_user(
          email = form.cleaned_data['email'],
          password  = form.cleaned_data['password1']
        )
        if user is not None:
          login(request,user)
          return redirect('welcome')
      else:
        messages.info(request, 'las contraseñas no coinciden :/')

    context = {
      'form': form,
      'msg':'login failed'
    }
    return render(request,self.template_name,context = context)