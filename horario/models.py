from django.db import models
from django.contrib.auth.models import User

class Aula(models.Model):
    titulo = models.CharField(max_length=100)
    instrutor = models.CharField(max_length=100)
    inicio = models.TimeField()
    fim = models.TimeField()
    dia = models.DateField(default=None)  # Data da aula
    max_alunos = models.IntegerField()

    def __str__(self):
        return self.titulo
    
    def vagas_disponiveis(self):
        return self.max_alunos - self.reservas.count()
    
    def aula_dia(self):
        return self.dia.year

    def aula_hora(self):
        return self.dia.strftime('%H:%M')

class Reserva(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.aula.titulo}"

class Horario(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    dia_da_semana = models.CharField(max_length=20, choices=[
        ('Segunda', 'Segunda-feira'),
        ('Terça', 'Terça-feira'),
        ('Quarta', 'Quarta-feira'),
        ('Quinta', 'Quinta-feira'),
        ('Sexta', 'Sexta-feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo')
    ])
    hora_inicio = models.TimeField()
