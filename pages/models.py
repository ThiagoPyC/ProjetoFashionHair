# O Django fornece automaticamente uma API(Interface de programação de aplicações) de abstração de banco de dados que permite criar, recuperar, atualizar e excluir objetos.
from django.db import models
from django.contrib.auth.models import User # User são objetos nucleos do sistema de Autenticação.

# Classe Cliente e seus atributos.
class cliente(models.Model):
    user = models.OneToOneField(
        verbose_name="Usuário", related_name='cliente',
        to=User, on_delete=models.PROTECT
    )
    senha = models.CharField("senha", max_length=30)
    nome = models.CharField("nome", max_length=100)
    email = models.EmailField("email", max_length=200)
    celular = models.CharField("celular", max_length=30)
    def __str__(self):
        return self.nome

# Classe Serviço e seus atributos.
class servico(models.Model):
    nome = models.CharField("nome", max_length=30)
    valor = models.DecimalField("valor", max_digits=5, decimal_places=2)

    def __str__(self):
         return self.nome

# Classe cabeleireiro e seus atributos.
class cabeleireiro(models.Model):
    user = models.OneToOneField(
        verbose_name="Usuário", related_name='cabeleireiro',
        to=User, on_delete=models.PROTECT
    )
    #apelido = models.CharField("apelido", max_length=100)
    email = models.EmailField("email", max_length=100)
    nome = models.CharField("nome", max_length=30)
    celular = models.CharField("celular", max_length=30)

    ativo = models.BooleanField(
    default=False
    )
    def __str__(self):
        return self.nome

# Classe Agendamento e seus atributos.
class agendamento(models.Model):
    STATUS_CHOICES = (
        ("Agendado", "Agendando"),
        ("Cancelado", "Cancelado"),
        ("Faltou", "Faltou"),
    )
    status = status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default="Agendado")
    data = models.DateField("data", help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    hora_inicio = models.TimeField("hora_inicio")
    hora_fim = models.TimeField("hora_fim")
    url = models.URLField("url", null=True,blank=True,max_length=500, default="127.0.0.1:8000/dashboard")
    clientes = models.ForeignKey(
        cliente,
		related_name='clientes',
        on_delete=models.CASCADE
    )
    cabeleireiros = models.ForeignKey(
        cabeleireiro,
		related_name='cabeleireiros',
        on_delete=models.CASCADE
    )
    servicos = models.ManyToManyField(
        servico,
        related_name='servicos',
    )

    
    def __str__(self):
        return self.data
