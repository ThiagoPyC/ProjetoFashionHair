from django.urls import path
from django.contrib.auth.urls import views as auth_views



from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    #path("servico", views.ServicoPageView.as_view(), name="servico"),
    path("servico", views.indexServico, name="servico"),

    #Login
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar', views.register_page, name='cadastrar'),

    # Agenda
    path('agenda/', views.indexCreate, name='indexCreate'),
    path('agenda/create', views.createAgenda, name='create'),
    path('agenda/deletar/<int:id>', views.deleteAgendamento, name='deleteAgendamento'),

    # Cabeleireiro
    path('cabeleireiro', views.indexcabeleireiro, name='indexcabeleireiro'),

    # Cliente
    path('cliente/', views.indexCliente, name='indexcliente'),
    path('cliente/create', views.createCliente, name='createCliente'),
    


]