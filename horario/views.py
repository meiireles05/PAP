from django.shortcuts import render, get_object_or_404, redirect
from .models import Reserva, Aula
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from homepage.models import Perfil
# Vista para exibir o horário semanal


def horario_semanal(request):
    # Obter a data atual ou a data selecionada pelo utilizador

    user = request.user
    
    hoje = datetime.today()
    data_selecionada = request.GET.get('data', f"{hoje.year}-{hoje.month:02d}-{hoje.day:02d}")
    data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d')

    # Calcular o início da semana (segunda-feira)
    inicio_da_semana = data_selecionada - timedelta(days=data_selecionada.weekday())
    dias_da_semana = [(inicio_da_semana + timedelta(days=i)) for i in range(7)]

    # Horas do dia (De 08:00 às 21:00)
    horas_do_dia = [f"{h:02}:00" for h in range(8, 22)]

    # Obter aulas entre os dias da semana selecionados
    #aulas = Aula.objects.filter(dia__range=[dias_da_semana[0], dias_da_semana[-1]])
    aulas = Aula.objects.all()
    for aula in aulas:
        aula.reservada = Reserva.objects.filter(aula=aula, usuario=user).exists()

    # Criar a lista de meses para o seletor de data
    meses = []
    for i in range(1, 13):
        primeiro_dia_do_mes = data_selecionada.replace(month=i, day=1)
        # Construir as strings manualmente
        meses.append({
            'valor': f"{primeiro_dia_do_mes.year}-{primeiro_dia_do_mes.month:02d}-01",
            'nome': f"{primeiro_dia_do_mes.year}-{primeiro_dia_do_mes.month:02d}",  # Nome mais simples
        })

    # Datas para navegação (sem `strftime`)
    semana_anterior = data_selecionada - timedelta(days=7)
    proxima_semana = data_selecionada + timedelta(days=7)

    return render(request, 'horario_semanal.html', {
        'dias_da_semana': dias_da_semana,
        'horas_do_dia': horas_do_dia,
        'aulas': aulas,
        'data_selecionada': f"{data_selecionada.year}-{data_selecionada.month:02d}-{data_selecionada.day:02d}",
        'semana_anterior': f"{semana_anterior.year}-{semana_anterior.month:02d}-{semana_anterior.day:02d}",
        'proxima_semana': f"{proxima_semana.year}-{proxima_semana.month:02d}-{proxima_semana.day:02d}",
        'meses': meses,  # Lista de meses já formatada
    })

# Vista para detalhes da aula
def detalhes_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    return render(request, 'detalhes_aula.html', {'aula': aula})

# Vista para marcar uma reserva
@login_required
def reservar_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    reserva_existente = Reserva.objects.filter(aula=aula, usuario=request.user).first()

    if request.method == 'POST':
        # Se o utilizador já tiver reserva, cancelar a reserva
        if 'cancelar' in request.POST:
            if reserva_existente:
                reserva_existente.delete()
                return redirect('horario_semanal')

        # Caso contrário, criar uma nova reserva
        elif 'reservar' in request.POST:
            if aula.vagas_disponiveis() > 0 and not reserva_existente:
                reserva = Reserva(aula=aula, usuario=request.user)
                reserva.save()
                return redirect('horario_semanal')
            else:
                return render(request, 'erro.html', {'mensagem': 'Não é possível reservar esta aula!'})

    return render(request, 'reservar_aula.html', {
        'aula': aula,
        'reserva_existente': reserva_existente
    })


@login_required
def criar_aula(request):
    # Check if user is type 1
    if request.user.perfil.tipo != '1':
        return redirect('horario_semanal')  # Redirect unauthorized users

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        instrutor = request.POST.get('instrutor')
        dia = request.POST.get('dia')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        max_alunos = request.POST.get('max_alunos')

        # Create the aula
        Aula.objects.create(
            titulo=titulo,
            instrutor=instrutor,
            dia=datetime.strptime(dia, '%Y-%m-%d').date(),
            inicio=datetime.strptime(inicio, '%H:%M').time(),
            fim=datetime.strptime(fim, '%H:%M').time(),
            max_alunos=int(max_alunos)
        )

        return redirect('horario_semanal')

    # Pass context to display the form
    dia = request.GET.get('dia')
    hora = request.GET.get('hora')  # Pre-fill the time field if clicked from the calendar
    return render(request, 'criar_aula.html', {'dia': dia, 'hora': hora})

