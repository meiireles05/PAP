from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo_recuperacao = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class PaymentTransaction(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pendente'),
        ('completed', 'Completado'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado')
    )

    PAYMENT_METHOD = (
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pagamento {self.transaction_id} - {self.status}"



class Horario(models.Model):
    # Salva data e hora completas
    data_hora = models.DateTimeField(default=timezone.now)
    