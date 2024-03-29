from django.db import models
from django.contrib.auth.models import User

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


class servico(models.Model):
    nome = models.CharField("nome", max_length=30)
    valor = models.DecimalField("valor", max_digits=5, decimal_places=2)
    url = models.URLField("url", null=True,blank=True,max_length=500)

    def __str__(self):
        return self.nome

class cabeleireiro(models.Model):
    user = models.OneToOneField(
        verbose_name="Usuário", related_name='cabeleireiro',
        to=User, on_delete=models.PROTECT
    )
    apelido = models.CharField("apelido", max_length=100)
    email = models.EmailField("email", max_length=100)
    nome = models.CharField("nome", max_length=30)
    #senha = models.CharField("senha", max_length=200)
    celular = models.CharField("celular", max_length=30)
    ativo = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.nome

class agendamento(models.Model):
    status = models.CharField("status", max_length=30, default = 'Agendado')
    data = models.DateField("data", help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    hora_inicio = models.TimeField("hora_inicio")
    hora_fim = models.TimeField("hora_fim")
    #url = models.URLField("url", null=True,blank=True,max_length=500)
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
        return self.status


