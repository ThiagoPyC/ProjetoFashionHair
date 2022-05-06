from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import servico, agendamento, cabeleireiro, cliente
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from .forms import RegisterForm




#@login_required



class HomePageView(TemplateView):
    template_name = 'home.html'


#class ServicoPageView(LoginRequiredMixin, TemplateView):
#    template_name = 'servico.html'

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
                    "form": form
              }
    if request.method == 'POST':
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
    
## clientes
@login_required
def indexCliente(request):
    clientes = cliente.objects.all()
    context = {'clientes' : clientes}
    return render(request, 'cliente/index.html',context)


@login_required
def createCliente(request):
    clientes = cliente()
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        new_user = User.objects.create_user(username, email, password)
        clientes.user = new_user
        clientes.email = email
        clientes.senha = password
        clientes.apelido = username
        clientes.nome = request.POST['nome']
        clientes.celular =  request.POST['celular']
        clientes.save()
        return HttpResponseRedirect('/cliente')
    else:
        return render(request, 'cliente/create.html')

@login_required
def indexServico(request):
    servicos = servico.objects.all()
    context = {'servicos' : servicos}
    return render(request, 'servico.html',context)


@login_required
def indexcabeleireiro(request):
    cabeleireiros = cabeleireiro.objects.all()
    context = {'cabeleireiros': cabeleireiros}
    return render(request, 'cabelereiro/indexcabelereiro.html', context)


@login_required
def indexCreate(request):
    agendamentos = agendamento.objects.all()
    clientes = cliente.objects.all()
    servicos = servico.objects.all()
    cabeleireiros = cabeleireiro.objects.all()
    context = {'agendamentos' : agendamentos, 'clientes' : clientes,'servicos' : servicos,'cabeleireiros' : cabeleireiros}
    return render(request, 'agenda/indexCreate.html',context)

@login_required
def createAgenda(request):

    agendamentos = agendamento()
    if request.method == 'POST':
        data_form = request.POST['data']
        hr_form = request.POST['hora_inicio'] + ':00'
        dates = date.today()
        if data_form < str(dates):
            messages.warning(request, 'Data menor/inferior a data atual. Escolha outra data!')
            return HttpResponseRedirect('/agenda/create')
        else:
            agendamentos_datas = agendamento.objects.filter(data=data_form)
            for aged in agendamentos_datas:
                if str(aged.hora_inicio) == hr_form:
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
            return HttpResponseRedirect('/agenda')
    else:
        clientes = cliente.objects.all()
        servicos = servico.objects.all()
        cabeleireiros = cabeleireiro.objects.all()
        context = {'servicos' : servicos,'cabeleireiros' : cabeleireiros}
        return render(request, 'agenda/create.html',context)

@login_required
def deleteAgendamento(request, id):
    agendamentos = agendamento.objects.get(id=id)
    agendamentos.delete()
    return redirect('/agenda')