from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegistroForm, PaymentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Perfil
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return render(request, 'home.html')
            else:
                messages.error(request, 'Utilizador ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home_view(request):
    return render(
        request, 
        'home.html',
        { 'logado':False, }
    )

def login_view2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        # Lógica para processar o registro
        pass
    return render(request, 'register.html')

def password_recovery(request):
    return render(request, 'password_recovery.html')
    
def logout_view(request):
    logout(request)
    return render(request, 'home.html')  



def schedule_view(request):
    return render(request, 'schedule.html')


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redireciona para uma página de sucesso
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def obter_perfil(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario_id=usuario_id)
    dados = {
        'username': perfil.usuario.username,
        'email': perfil.usuario.email,
        'bio': perfil.bio,
        'telefone': perfil.telefone,
        'foto': perfil.foto.url if perfil.foto else '',
    }
    return JsonResponse(dados)


def obter_perfil(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Tente obter o perfil associado ao usuário (assumindo que você tenha um modelo Perfil)
    try:
        perfil = usuario.perfil  # Ajuste conforme o nome do seu modelo de perfil
        bio = perfil.bio if hasattr(perfil, 'bio') else ''
        telefone = perfil.telefone if hasattr(perfil, 'telefone') else ''
        foto = perfil.foto.url if hasattr(perfil, 'foto') and perfil.foto else ''
    except:
        bio = ''
        telefone = ''
        foto = ''
    
    dados = {
        'username': usuario.username,
        'email': usuario.email,
        'bio': bio,
        'telefone': telefone,
        'foto': foto,
    }
    return JsonResponse(dados)