from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, FloatField
from django.http import HttpResponse
# Create your views here.
from Site.forms import UserForm,RemoveUserForm, ProdutoForm, AtualizaProdutoForm, RemoveProdutoForm,ColocaProdutoCarrinhoForm
from Site.models import Images, User, Produto
from Site.carrinho import  Carrinho
import json


def home(request):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='Home'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    return render(request, 'Home/index.html',{'caminhos':caminhos} )


def noticia(request):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='Home_Bar'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='noticia'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    return render(request, 'Noticia/noticia.html', {'caminhos':caminhos})

def login(request):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    return render(request, 'login/login.html', {'caminhos':caminhos})



def cadastra_User(request):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='cadastro'):
        caminhos[item.nome] = "images/" + item.caminho
    # Aqui recuperamos o parâmetro de requisição produto_id.
    # Se este parâmetro de requisição existir no objeto request, significa que se trata de uma alteração.
    # Caso contrário, trata-se de uma inclusão.
    User_id = request.POST.get('id')
    print("User_id")
    print(User_id)
    if request.POST:
        # Se o parâmetro veio, trata-se de uma alteração.
        if User_id:
            acao = 'alteracao'
            # Recupera um objeto Produto ou gera o erro 404
            user = get_object_or_404(User, pk=User_id)

            # Como se trata de uma alteração, o objeto ProdutoForm é instanciado utilizando
            # os dados provenientes do banco de dados (instance=produto) e, em seguida,
            # essas informações são atualizadas utilizando os dados submetidos pelo usuário (request.POST).
            form_user = UserForm(request.POST, instance=user)
        else:

            acao = 'inclusao'
            form_user = UserForm(request.POST)

        # A linha de código abaixo testa se os dados constantes do form estão corretos.
        # As regras de validação foram definidas no form (ProdutoForm). Os campos categoria, nome, preco e
        # data_cadastro são de preenchimento obrigatório (required=True). E o campo preco deve obedecer a
        # uma expressão regular (veja em ProdutoForm)

        # Observe que o comando if abaixo não possui o "else". Caso ocorra um erro de validação a página
        # cadastra_produto.html será exibida novamente juntamente com as mensagens de erro.
        if form_user.is_valid():
            print("VALIDO")
            # O método save() de ModelForm salva o produto (inclui ou altera) no banco de dados e retorna
            # um objeto do tipo Produto.
            user = form_user.save()

            # Se a variável produto_id for diferente de None então trata-se de uma alteração
            if User_id:
                # Gera uma mensagem que será exibida pela página exibe_produto.html através do framework de mensagens.
                messages.add_message(request, messages.INFO, 'Usuário alterado com sucesso.')
            else:
                messages.add_message(request, messages.INFO, 'Usuário cadastrado com sucesso.')

            # Aqui efetuamos um redirect para evitar que um mesmo produto seja cadastrado mais
            # de uma vez caso o usuário aperte a tecla F5 após cadastrar o produto.
            return redirect('Site:exibe_user', id=user.id)
        else:
            print("NAO VALIDO")
            return render(request, 'Cadastro/cadastra_user.html',{'form': form_user, 'acao': acao, 'caminhos': caminhos})

    else:
        # Ao chegar uma requisição do tipo GET, a página cadastra_produto.html é exibida.
        acao = 'inclusao'

        form_user = UserForm()

    # Caso ocorra um erro de validação a página cadastra_produto.html será exibida com as
    # mensagens de erro de validação.
    return render(request, 'Cadastro/cadastra_user.html', {'form': form_user, 'acao': acao,'caminhos':caminhos})


def exibe_user(request, id):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='exibir'):
        caminhos[item.nome] = "images/" + item.caminho
    user = get_object_or_404(User, pk=id)
    # Aqui instanciamos o objeto remove_produto_form para que os botões de edição e de remoção sejam exibidos.
    return render(request, 'Cadastro/exibe_usuario.html', {'user': user,'remove_user_form': id,'caminhos':caminhos})


def edita_user(request, id):
    caminhos = {}
    for item in Images.objects.filter(nome__contains='base'):
        caminhos[item.nome] = "images/" + item.caminho
    for item in Images.objects.filter(nome__contains='cadastro'):
        caminhos[item.nome] = "images/" + item.caminho
    user = get_object_or_404(User, pk=id)
    form_user = UserForm(instance=user)
    form_user.fields['id'].initial = user.id
    return render(request, 'Cadastro/cadastra_user.html', {'form': form_user,'acao': 'alteracao','caminhos':caminhos})


def remove_user(request):
    print("REMOVE")
    User_id = request.POST.get('User_id')
    print(User_id)
    remove_user_form = RemoveUserForm(request.POST)
    if remove_user_form.is_valid():
        print("REMOVE2")

        print("REMOVE3")
        user = get_object_or_404(User, pk=User_id)
        print("REMOVE4")
        user.delete()
        print("REMOVE5")
        messages.add_message(request, messages.INFO, 'Usuário removido com sucesso.')
        return render(request, 'Cadastro/exibe_usuario.html', {'user': user, 'remove_usuario_form': None})
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um Usuário')





def cadastra_produto(request):

    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            produto = form.save(commit=False)
            produto.user=request.user
            produto.save()

            lista = Produto.objects.all()

            lista_de_produtos = []
            valor_do_estoque = 0
            for prod in lista:
                valor_do_estoque = valor_do_estoque + prod.preco * prod.estoque
                if produto.id == prod.id:
                    lista_de_produtos.append({'produto': produto,
                                              'form': AtualizaProdutoForm(initial={'estoque': produto.estoque})})

            return render(request, 'produto/lista_de_produtos.html', {'lista_de_produtos': lista_de_produtos,
                                                                      'valor_do_estoque': valor_do_estoque})

    else:
        form = ProdutoForm()

    produtos = Produto.objects.all()

    lista_de_produtos = []
    valor_do_estoque = 0
    ids_dos_produtos = []
    for produto in produtos:
        valor_do_estoque = valor_do_estoque + produto.preco * produto.estoque
        ids_dos_produtos.append(produto.id)
        lista_de_produtos.append({'produto': produto,
                                  'form': AtualizaProdutoForm(initial={'estoque': produto.estoque})})

    return render(request, 'produto/cadastra_produto.html', {'form': form,
                                                             'lista_de_produtos': lista_de_produtos,
                                                             'ids_dos_produtos': ids_dos_produtos,
                                                             'valor_do_estoque': valor_do_estoque})


def remove_produto(request):
    print('Entrou em remove_produto')
    form = RemoveProdutoForm(request.POST)
    if form.is_valid():
        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
        print(produto)
        if request.user == produto.user:
            produto.delete()

        # A linha de código abaixo irá retornar none para resultado['valor_do_estoque'] caso a soma do produto
        # (estoque * preco) seja igual a zero. Por essa razão acrescentei o if ... else ... abaixo.
        resultado = Produto.objects.filter(disponivel=True).aggregate(valor_do_estoque=Sum(F('estoque')*F('preco'), output_field=FloatField()))

        if resultado['valor_do_estoque']:
            return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': '{0:.2f}'.format(resultado['valor_do_estoque'])})
        else:
            return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': '0,00'})
        # return HttpResponse("{0:.2f}".format(resultado['valor_do_estoque']).replace('.',','))
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um produto!')

def atualiza_produto(request):
    form = AtualizaProdutoForm(request.POST)
    if form.is_valid():
        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
        produto.estoque = form.cleaned_data['estoque']
        produto.save()

        resultado = Produto.objects.filter(disponivel=True).aggregate(valor_do_estoque=Sum(F('estoque')*F('preco'), output_field=FloatField()))
        return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': "{0:.2f}".format(resultado['valor_do_estoque'])})
        # return HttpResponse("{0:.2f}".format(resultado['valor_do_estoque']).replace('.',','))
    else:
        print(form.errors)
        raise ValueError('Ocorreu um erro inesperado ao tentar alterar um produto!')

def lista_produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'Vendas/pesquisa_produto.html', {'lista_de_produtos': produtos})

def exibe_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)

    # Aqui instanciamos o objeto remove_produto_form para que os botões de edição e de remoção sejam exibidos.
    remove_produto_form = RemoveProdutoForm(initial={'produto_id': id})
    return render(request, 'produto/exibe_produto.html', {'produto': produto,
                                                          'remove_produto_form': remove_produto_form})




def SalvaprodutoCarrinho(request):
    form = ColocaProdutoCarrinhoForm(request.POST)
    if form.is_valid():

        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
        carrinho = Carrinho(request)
        print(1)
        if carrinho.RetornaCotas(produto.id)>0:
            print(2)
            carrinho.adicionar(produto.id, form.cleaned_data['produto_qtd'])
        else:
            print(3)
            carrinho.adicionar(produto.id, form.cleaned_data['produto_qtd'])

        result = str(form.cleaned_data['produto_qtd']) + ' Cota de produtos Compradas, total de ' + str(carrinho.RetornaCotas(produto.id))
        print(result)
        return HttpResponse(json.dumps({'name':result}), content_type="application/json")
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar comprar cotas!')


def RemoveprodutoCarrinho(request):
    form = ColocaProdutoCarrinhoForm(request.POST)

    if form.is_valid():
        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
        estoque = -form.cleaned_data['produto_qtd']

        carrinho = Carrinho(request)
        carrinho.adicionar(produto.id, estoque)

        if carrinho.RetornaCotas(produto.id)==0 :
            result = 'Produto Removido do carrinho'
        else:
            result = str(form.cleaned_data['produto_qtd']) + ' cotas removidas do produto'

        return HttpResponse(json.dumps({'name':result}), content_type="application/json")
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar comprar cotas!')


def ListaCarrinho(request):
    carrinho = Carrinho(request)

    carrinhos = carrinho.get_lista_de_carrinhos()

    lista_de_carrinhos = []
    for item in carrinhos:

        produto = get_object_or_404(Produto, pk=item['id'])
        lista_de_carrinhos.append({'produto': produto,
                                  'cotas': carrinho.RetornaCotas(item['id']),
                                  'preco':carrinho.RetornaCotas(item['id']) * produto.preco})
    return render(request, 'vendas/Lista_carrinho.html', {'lista_de_carrinhos': lista_de_carrinhos})