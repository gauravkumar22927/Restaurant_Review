from django.shortcuts import render,redirect
from .forms import ExtendedUserCreationForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import JsonResponse

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

      return redirect('review')
  else:
    form = ExtendedUserCreationForm()
  context = {'form' : form}
  return render(request, "register.html",context)
#login
def login_page(request ,*args,**kwargs):
  return render(request, "login_page.html")

@login_required
def review_form(request ,*args,**kwargs):
  """
  if request.method == 'POST':
    form = ReviewForm(request.POST)

    if form.is_valid():
      form.save()
  else:
    form = ReviewForm()
  """
  form = ReviewForm()
  context = {"form" : form}
  return render(request, "review.html",context)

@login_required
def predict_chances(request,*args,**kwargs):
    if request.POST.get('action') == 'post':
        form = ReviewForm(request.POST)
        if form.is_valid():
          form.save()
        ## Receive data from client
        #food = float(request.POST.get('food'))
        #speed = float(request.POST.get('speed'))
        #price = float(request.POST.get('price'))
        #text = float(request.POST.get('text'))

        ## Unpickle model
        #model = pd.read_pickle(r"C:\Users\gaurav\OneDrive\Desktop\new_model.pickle")
        ## Make prediction
        #result = model.predict([[form.cleaned_data.get("text")]])

        #classification = result[0]

        #PredResults.objects.create(food=food, speed=speed, price=price,text=text, classification=classification)

        return JsonResponse({'result': "Positive", 'name': form.cleaned_data.get("name"),'food': form.cleaned_data.get("food"), 'speed':form.cleaned_data.get("speed"), 'price':form.cleaned_data.get("price"),'text': form.cleaned_data.get("text")},safe=False)