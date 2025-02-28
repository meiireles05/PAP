from django.urls import path
from .views import home_view
from django.contrib.auth import views as auth_views
from . import views

app_name='gym'

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', views.register_view, name='registro'),
    path('login/password_recovery', views.password_recovery, name='password_recovery'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('perfil/<int:usuario_id>/', views.obter_perfil, name='obter_perfil'),
    
]
