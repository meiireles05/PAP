from django.urls import path,include    
from .views import home_view
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

app_name='gym'

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', views.register_view, name='registro'),
    path('login/password_recovery', views.password_recovery, name='password_recovery'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/loginsuccess.html/', views.loginsuccess, name='success_url')
]
