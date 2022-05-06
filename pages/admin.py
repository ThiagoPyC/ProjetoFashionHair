from django.contrib import admin

from .models import (
    servico,
    agendamento,
    cabeleireiro,
    cliente,
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
    list_display = ['status', 'data', 'hora_inicio', 'hora_fim', 'cabeleireiros']
    search_fields = ['status', 'data', 'hora_inicio', 'hora_fim','cabeleireiros']

