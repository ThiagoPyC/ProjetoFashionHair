# Forms.py são arquivos de formulario para autenticação.
from django import forms
from django.contrib.auth import get_user_model 

#get_user_model é o modelo de usuario que está ativo no momento
User = get_user_model()

# Classe e atributos para Registrar o Usuarios
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    # Metedo para quando o usurio se registrar e esse usuario já existir retornar a mensagem abaixo.
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Esse usuário já existe, escolha outro nome.")
        return username

    # Metedo para quando o usurio se registrar e esse email já existir retornar a mensagem abaixo
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Esse email já existe, tente outro!")
        return email

    # Metedo para quando o usurio se registrar e esse usuario já existir retornar a mensagem abaixo
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("As senhas informadas devem ser iguais!")
        return data

# claned_data = retorna um dicionário de campos de entrada de formulário validados e seus valores, 
# onde as chaves primárias de string são retornadas como objetos.