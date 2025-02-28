from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Payment  # Import the Payment model


class RegistroForm(UserCreationForm):
    # Formulario de registro de usuario
    
    class Meta:
        model = User
        fields = ("username", "password", "password1")


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'email', 'card_number', 'expiry_date']

