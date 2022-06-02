from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required #Se o usuário não estiver logado, redirecione para settings.LOGIN_URL, passando o caminho absoluto atual na string de consulta.
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import servico, agendamento, cabeleireiro, cliente # Importando os models.py(classes).
from django.shortcuts import render, redirect # render = renderizar o html, redirect = redirecionar para o html.
from django.http import HttpResponseRedirect
from django.contrib import messages # messages = mensagem de error.
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from .forms import RegisterForm # Importando os forms.py(formulario de registro)
from django.http import JsonResponse # JsonResponse é uma subclasse HttpResponse que ajuda a criar uma resposta codificada em JSON


class HomePageView(TemplateView):
    template_name = 'home.html'

User = get_user_model() #get_user_model é o modelo de usuario que está ativo no momento

# Função para registrar o Usuario.
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
                    "form": form
              }
    if request.method == 'POST':  # Objeto de requisições
        if form.is_valid():
            print(form.cleaned_data)
            print(">>>>>>>>>>>>>", form.cleaned_data)
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            new_user = User.objects.create_user(username, email, password)
            nome = request.POST['nome']
            celular = request.POST['celular']
            cli = cliente(
                user=new_user,
                nome=nome,
                celular=celular,
                senha=password,
                email=email
            )
            cli.save()
            return render(request, 'registration/login.html', context)
        else:
            return render(request, "registration/register.html", context)
    return render(request, "registration/register.html", context)

# Função para Tela serviço, aqui estou pegando da classe serviço seus atributos e chamando todos os objetos que estão em serviço
@login_required
def indexServico(request):
    servicos = servico.objects.all()
    context = {'servicos' : servicos}
    return render(request, 'servico.html',context)

@login_required
def indexcabeleireiro(request):
    cabeleireiros = cabeleireiro.objects.all()
    #servicos = servico.objects.all()
    context = {'cabeleireiros': cabeleireiros}
    return render(request, 'cabelereiro/indexcabelereiro.html', context)


# Função para Tela Minha Agenda, aqui estou pegando todos os objetos de agendamento relacionados ao get_user_model(usuario que está ativo no momento).
@login_required
def indexCreate(request):
    agendamentos = agendamento.objects.all()
    clientes = cliente.objects.all()
    servicos = servico.objects.all()
    cabeleireiros = cabeleireiro.objects.all()
    context = {'agendamentos' : agendamentos, 'clientes' : clientes, 'servicos' : servicos,'cabeleireiros' : cabeleireiros}
    return render(request, 'agenda/indexCreate.html',context)

# Função para Tela de Criar agendamento.
@login_required
def createAgenda(request):

    agendamentos = agendamento()
    if request.method == 'POST':
        data_form = request.POST['data']
        hr_form = request.POST['hora_inicio'] + ':00'
        dates = date.today()
        if data_form < str(dates): # Metodo para saber se a data é inferior a data atual
            messages.warning(request, 'Data menor/inferior a data atual. Escolha outra data!')
            return HttpResponseRedirect('/agenda/create')      
        else:
            agendamentos_datas = agendamento.objects.filter(data=data_form)
            for aged in agendamentos_datas:
                if str(aged.hora_inicio) == hr_form: # Metodo para saber se existe um agendamento já marcado no Horario escolhido.
                    messages.warning(request, 'Já tem agendamento nesse horario')
                    return HttpResponseRedirect('/agenda/create')
            
            servicos = servico.objects.get(id=int(request.POST['servico']))
            clientes = cliente.objects.get(id=int(request.POST['cliente']))
            cabeleireiros = cabeleireiro.objects.get(id=int(request.POST['cabeleireiro']))
            agendamentos.data = request.POST['data']
            agendamentos.hora_inicio = request.POST['hora_inicio']
            hora_inicio = request.POST['hora_inicio']
            data_e_hora_em_texto = hora_inicio
            data = datetime.strptime(data_e_hora_em_texto, "%H:%M") + timedelta(minutes=30)
            hora = data.strftime("%H:%M")
            agendamentos.hora_fim = hora
            agendamentos.clientes = clientes
            agendamentos.cabeleireiros = cabeleireiros
            agendamentos.save()
            agendamentos.servicos.add(servicos)
            clientes = cliente.objects.all()
            servicos = servico.objects.all()
            cabeleireiros = cabeleireiro.objects.all()
            # Um Contexto é um dicionário com nomes de variáveis ​​como chave e seus valores como valor, onde eu consigo chamar os valores da classes e chamar no HTML.
            context = {'clientes': clientes, 'servicos' : servicos,'cabeleireiros' : cabeleireiros} 
            return HttpResponseRedirect('/agenda')
    else:
        clientes = cliente.objects.all()
        servicos = servico.objects.all()
        cabeleireiros = cabeleireiro.objects.all()
        context = {'servicos' : servicos,'cabeleireiros' : cabeleireiros}
        return render(request, 'agenda/create.html',context)

# Função onde o usuario cancela o Agedamento
@login_required
def deleteAgendamento(request, id):
    agendamentos = agendamento()    
    agendamentos = agendamento.objects.get(id=id)
    agendamentos.delete()
    return redirect('/agenda')

# Chamando o Calendario
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar.html'
    extra_context = {
        'cabeleireiros': cabeleireiro.objects.all(),
        'servicos': servico.objects.all(),
    }

# Retornando os objetos que estarão na tela do Calendario
def get_data(request):
    data = []
    for agend in agendamento.objects.all():
        d = agend.data
        hi = agend.hora_inicio
        hf = agend.hora_fim
        nome = agend.clientes.nome
        #serv = agend.servicos.all
        data.append(
            dict(title=f'{hi:%H:%M} - {hf:%H:%M}' + '\n' + nome,
                 start=f'{d:%Y-%m-%d} {hi:%H:%M}', 
                 end=f'{d:%Y-%m-%d} {hf:%H:%M}',
                 allDay=False,
                 className='event-azure'
                 ),
        )
    print(data)
    return JsonResponse(data, safe=False)