from django.shortcuts import render,redirect
from .forms import ExtendedUserCreationForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import JsonResponse

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Model # new! pip install tensorflow
from keras.layers import Input, concatenate # new! 
from keras.layers import Dense, Dropout, Embedding, SpatialDropout1D, Conv1D, GlobalMaxPooling1D
import os
#global helper function attributes

# output directory name:
output_dir = 'model_output/multiconv'
# vector-space embedding: 
n_dim = 64
n_unique_words = 1581 
max_review_length = 106
pad_type = trunc_type = 'pre'
drop_embed = 0.2 
# convolutional layer architecture:
n_conv_1 = n_conv_2 = n_conv_3 = 256 
k_conv_1 = 3
k_conv_2 = 2
k_conv_3 = 4
# dense layer architecture: 
n_dense = 256
dropout = 0.2

input_layer = Input(shape=(max_review_length,), dtype='int16', name='input')  
embedding_layer = Embedding(n_unique_words, n_dim, input_length=max_review_length, name='embedding')(input_layer)
drop_embed_layer = SpatialDropout1D(drop_embed, name='drop_embed')(embedding_layer)

conv_1 = Conv1D(n_conv_1, k_conv_1, activation='relu', name='conv_1')(drop_embed_layer)
maxp_1 = GlobalMaxPooling1D(name='maxp_1')(conv_1)

conv_2 = Conv1D(n_conv_2, k_conv_2, activation='relu', name='conv_2')(drop_embed_layer)
maxp_2 = GlobalMaxPooling1D(name='maxp_2')(conv_2)

conv_3 = Conv1D(n_conv_3, k_conv_3, activation='relu', name='conv_3')(drop_embed_layer)
maxp_3 = GlobalMaxPooling1D(name='maxp_3')(conv_3)

concat = concatenate([maxp_1, maxp_2, maxp_3])

dense_layer = Dense(n_dense, activation='relu', name='dense')(concat)
drop_dense_layer = Dropout(dropout, name='drop_dense')(dense_layer)
dense_2 = Dense(64, activation='relu', name='dense_2')(drop_dense_layer)
dropout_2 = Dropout(dropout, name='drop_dense_2')(dense_2)

predictions = Dense(1, activation='sigmoid', name='output')(dropout_2)

model = Model(input_layer, predictions) #tensorflow , keras
model.load_weights(output_dir+"/weights.73.hdf5")

#end of global attributes

import re
import pickle 
from nltk.stem.porter import PorterStemmer
with open('saved_dictionary.pkl', 'rb') as f:
    dict_word = pickle.load(f)

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

      return redirect('myapp:review')
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


def pred_helper(text):
  
  review_custom = re.sub('[^a-zA-Z]', ' ', text) #input text 
  review_custom = review_custom.lower()
  review_custom = review_custom.split()
  ps = PorterStemmer()
  review_custom = [ps.stem(word) for word in review_custom]
  review_custom = ' '.join(review_custom)

  custom_list = []
  custom_test = []
  for x in review_custom.split():
      if(x in dict_word.keys()):
          custom_test.append(dict_word[x])
  custom_list.append(custom_test)

  custom_list = np.array(custom_list) #numpy
  custom_list = pad_sequences(custom_list, maxlen=max_review_length, padding=pad_type, truncating=trunc_type, value=0)
  pred_1 = model.predict(custom_list)

  if(pred_1[0][0] < 0.4):
    return "Negative"
  elif(pred_1[0][0] < 0.9):
    return "Average"
  else:
    return "Positive"

  
@login_required
def predict_chances(request,*args,**kwargs):
    if request.POST.get('action') == 'post':
        form = ReviewForm(request.POST)
        if form.is_valid():
          form.save()
        # Receive data from client
        #food = form.cleaned_data.get("food")
        #speed = form.cleaned_data.get("speed")
        #price = form.cleaned_data.get("price")
        text = form.cleaned_data.get("text")

        ## Unpickle model
        #model = pd.read_pickle(r"C:\Users\gaurav\OneDrive\Desktop\new_model.pickle")
        ## Make prediction
        #result = model.predict([[form.cleaned_data.get("text")]])
        classification = pred_helper(text)

        #classification = result[0]

        #PredResults.objects.create(food=food, speed=speed, price=price,text=text, classification=classification)
        
        return JsonResponse({'result': classification , 'name': form.cleaned_data.get("name"),'food': form.cleaned_data.get("food"), 'speed':form.cleaned_data.get("speed"), 'price':form.cleaned_data.get("price"),'text': form.cleaned_data.get("text")},safe=False)