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
        #sepal_length = float(request.POST.get('sepal_length'))
        #sepal_width = float(request.POST.get('sepal_width'))
        #petal_length = float(request.POST.get('petal_length'))
        #petal_width = float(request.POST.get('petal_width'))

        ## Unpickle model
        #model = pd.read_pickle(r"C:\Users\azander\Downloads\new_model.pickle")
        ## Make prediction
        #result = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

        #classification = result[0]

        #PredResults.objects.create(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length,petal_width=petal_width, classification=classification)

        return JsonResponse({'result': "Positive", 'name': "dbaf",'food': "dfs", 'speed':"fdsg", 'price':"fsdg",'text':"restaurant was good"},
                            safe=False)