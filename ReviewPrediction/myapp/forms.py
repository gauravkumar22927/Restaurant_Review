from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.forms import ModelForm
from .models import Review

class ExtendedUserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ('username','email','password1','password2')
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['username'].widget.attrs.update({"id":"username-register", "name":"username", "class":"form-control", "type":"text", "placeholder":"Pick a username", "autocomplete":"off","tabindex":1})
    self.fields['email'].widget.attrs.update({"id":"email-register", "name":"email", "class":"form-control" ,"type":"text", "placeholder":"you@example.com", "autocomplete":"off","tabindex":2})
    self.fields['password1'].widget.attrs.update({"id":"password-register","name":"password1", "class":"form-control", "type":"password" ,"placeholder":"Create a password","tabindex":3})
    self.fields['password2'].widget.attrs.update({"id":"password-register","name":"password2", "class":"form-control", "type":"password" ,"placeholder":"Confirm password","tabindex":4})
    
  def save(self,commit = True):
    user = super().save(commit = False)
    user.email = self.cleaned_data['email']

    if commit:
      user.save()

    return user

class ExtendedAuthenticationForm(AuthenticationForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['username'].widget.attrs.update({"name":"username", "class":"form-control form-control-sm input-dark", "type":"text" ,"placeholder":"Username" ,"autocomplete":"off"})
    self.fields['password'].widget.attrs.update({"name":"password", "class":"form-control form-control-sm input-dark", "type":"password", "placeholder":"Password"})

class ReviewForm(ModelForm):
  class Meta:
    model = Review
    fields = ['name' , 'food' , 'speed' , 'price', 'text']

  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['name'].widget.attrs.update({"type":"text","id":"name", "name":"name", "placeholder":"Enter Name","tabindex":1})
    self.fields['food'].widget.attrs.update({"value":"none","id":"food", "name":"food","tabindex":2})
    self.fields['speed'].widget.attrs.update({"value":"none","id":"speed", "name":"speed","tabindex":3})
    self.fields['price'].widget.attrs.update({"value":"none","id":"price","name":"price","tabindex":4})
    self.fields['text'].widget.attrs.update({"id":"text","rows":"5","tabindex":5})
    
  def save(self,commit = True):
    review = super().save(commit = False)

    if commit:
      review.save()

    return review