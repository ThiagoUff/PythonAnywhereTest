from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'Site'


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('noticia/', views.noticia, name='noticia'),
    path('login/', views.login, name='login'),
    path('cadastrar/', views.cadastra_User, name='cadastra_User'),
    path('exibirUser/<int:id>/', views.exibe_user, name='exibe_user'),
    path('editar/<int:id>/', views.edita_user, name='edita_user'),
    path('remover/', views.remove_user, name='remove_user'),

    path('cadastra_produto/', views.cadastra_produto, name='cadastra_produto'),
    path('remove_produto/', views.remove_produto, name='remove_produto'),
    path('atualiza_produto/', views.atualiza_produto, name='atualiza_produto'),
    path('listar_produto/', views.lista_produtos, name='lista_produtos'),
    path('exibir/<int:id>/', views.exibe_produto, name='exibe_produto'),

    path('SalvaprodutoCarrinho/', views.SalvaprodutoCarrinho, name='SalvaprodutoCarrinho'),
    path('RemoveprodutoCarrinho/', views.RemoveprodutoCarrinho, name='RemoveprodutoCarrinho'),

    path('Carrinho/',views.ListaCarrinho,name='ListaCarrinho'),
]
