from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegistroForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import PaymentTransaction
import uuid
from .forms import Login_Form


@login_required
def payment_process(request):
    if request.method == 'POST':
        # Gerar ID único para a transação
        transaction_id = str(uuid.uuid4())
        
        try:
            # Criar nova transação
            transaction = PaymentTransaction.objects.create(
                user=request.user,
                amount=request.POST.get('amount'),
                payment_method=request.POST.get('payment_method'),
                transaction_id=transaction_id,
                description=request.POST.get('description')
            )
            
            # Aqui você pode adicionar a integração com um gateway de pagamento
            # Por exemplo: Stripe, PayPal, etc.
            
            # Simular processamento bem-sucedido
            transaction.status = 'completed'
            transaction.save()
            
            return JsonResponse({
                'status': 'success',
                'transaction_id': transaction_id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return render(request, 'payment.html')

@login_required
def payment_history(request):
    transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payment.html', {'transactions': transactions})



@login_required
def logout_view(request):
    logout(request)
    request.user = None
    return redirect(home_view)

# Create your views here.



def home_view(request):
    return render(
        request, 
        'home.html',
    )

@ensure_csrf_cookie
def check_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'username': request.user.username
        })
    return JsonResponse({
        'isAuthenticated': False
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Process the login
            # Example: authenticate and login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'home.html', {'form': form})
            else:
                return render(request, 'login2.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login2.html', {'form': form})
   
   #if request.method == 'POST':
   #     username = request.POST.get('username')
   #     password = request.POST.get('password')
   #     messages.error(request, request.POST.get('username') + ' ' + request.POST.get('username'))
        #user = authenticate(request, username=username, password=password)
        
        #if user is not None:
        #    login(request, user)
        #    messages.success(request, 'Login realizado com sucesso!')
        #    return redirect('home')  # Redireciona para a página inicial após login
        #else:
        #    messages.error(request, 'Username ou password inválidos.')
    #else:
    return render(request, 'login.html')



#def registro_view(request):
#    if request.method == 'POST':
#        form = RegistroForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            login(request, user)
#            messages.success(request, 'Registro realizado com sucesso!')
#            return redirect('home')
#    else:
#        form = RegistroForm()
#    return render(request, 'registro.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'As passwords não coincidem.')
            return render(request, 'register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username já existe.')
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está em uso.')
            return render(request, 'register.html')
            
        # Criar novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Conta criada com sucesso! Faça login.')
        return redirect('/login.html')
        
    return render(request, 'register.html')

def password_recovery(request):
    return render(request, 'password_recovery.html')


def enviar_codigo_reset(email):
    # Implement your logic to send the reset code here
    # For example, you might send an email with the code
    # Return a tuple (success, message)
    return True, "Código de reset enviado com sucesso."

def solicitar_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verificar se o email existe
        if User.objects.filter(email=email).exists():
            sucesso, mensagem = enviar_codigo_reset(email)
            if sucesso:
                # Guardar email na sessão para usar na próxima etapa
                request.session['reset_email'] = email
                return redirect('confirmar_codigo')
            else:
                messages.error(request, mensagem)
        else:
            messages.error(request, "Email não encontrado.")
    
    return render(request, 'reset_password/solicitar.html')


def verificar_codigo_reset(email, codigo):
    # Implement your logic to verify the reset code here
    # For example, you might check the code against a database or cache
    # Return True if the code is valid, otherwise return False
    return True  # Placeholder implementation



def confirmar_codigo(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('solicitar_reset_password')
        
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        if verificar_codigo_reset(email, codigo):
            request.session['codigo_verificado'] = True
            return redirect('nova_password')
        else:
            messages.error(request, "Código inválido ou expirado.")
    
    return render(request, 'reset_password/confirmar_codigo.html')

def nova_password(request):
    if not request.session.get('codigo_verificado'):
        return redirect('solicitar_reset_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            
            # Limpar dados da sessão
            del request.session['reset_email']
            del request.session['codigo_verificado']
            
            messages.success(request, "Password alterada com sucesso!")
            return redirect('login')
        else:
            messages.error(request, "As passwords não coincidem.")
    
    return render(request, 'reset_password/nova_password.html')


from django.shortcuts import render, redirect
from .forms import LoginForm

def loginview(request):
    # Se o usuário já está autenticado, redireciona para página de sucesso
    if request.user.is_authenticated:
        return render(request, 'pagina_bemvindo.html')
    
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'pagina_bemvindo.html')
            else:
                form.add_error(None, 'Credenciais inválidas')
    else:
        form = Login_Form()
    
    return render(request, 'login.html', {'form': form})


def loginsuccess(request):
    return render(request, 'loginsuccess.html')