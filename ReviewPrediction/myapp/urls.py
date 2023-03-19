from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import ExtendedAuthenticationForm

urlpatterns = [
    path('register/',views.register_page,name='register_page'),
    path('',auth_views.LoginView.as_view(template_name='login_page.html',authentication_form = ExtendedAuthenticationForm),name='login'),
    path('index/',views.index,name='index'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
]
