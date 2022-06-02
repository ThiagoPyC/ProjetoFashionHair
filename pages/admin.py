from django.contrib import admin

from .models import (
    servico,
    agendamento,
    cabeleireiro,
)

@admin.register(servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor']
    search_fields = ['nome', 'valor']


@admin.register(cabeleireiro)
class CabelereiroAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['nome', 'email']
    search_fields = ['nome', 'email']

@admin.register(agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['status', 'clientes','data', 'hora_inicio', 'hora_fim', 'cabeleireiros', 'url']
    search_fields = ['status','clientes','data', 'hora_inicio', 'hora_fim','cabeleireiros', 'url']


