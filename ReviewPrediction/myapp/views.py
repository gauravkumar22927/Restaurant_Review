from django.shortcuts import render,redirect
from .forms import ExtendedUserCreationForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

from django.http import HttpResponse

# Create your views here.
def register_page(request ,*args,**kwargs):
  if request.method == 'POST':
    form = ExtendedUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()

      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password1")

      user = authenticate(username = username,password = password )
      login(request,user)

      return redirect('index')
  else:
    form = ExtendedUserCreationForm()

  context = {'form' : form}

  return render(request, "register.html",context)

def login_page(request ,*args,**kwargs):
  return render(request, "login_page.html")

@login_required
def index(request ,*args,**kwargs):
  if request.method == 'POST':
    form = ReviewForm(request.POST)

    if form.is_valid():
      form.save()
  else:
    form = ReviewForm()
  form = ReviewForm()
  context = {"form" : form}
  return render(request, "review.html",context)
