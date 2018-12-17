from decimal import Decimal
from django.conf import settings

from Site.models import Produto

class Carrinho(object):

    def __init__(self, request):
        """ Initializa o carrinho de compras. """

        # Para que a sessão possa ser acessada por outros métodos
        self.session = request.session

        # recupera o carrinho da sessão e o salva na variável de instância carrinho
        self.carrinho = self.session.get(settings.CARRINHO_SESSION_ID)

        # Se a sessão não tiver um carrinho
        if not self.carrinho:
            # cria um carrinho vazio e o salva na sessão, e na variável de instância carrinho.
            # carrinho é um dicionário que irá conter pares de chave e valor. A chave será o id de um produto
            # e o valor será um dicionário contendo o id do produto, a quantidade e o preço.
            self.carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}

        # Observação:
        # -----------
        # Nosso dicionário para o carrinho deve utilizar ids dos produtos como chaves e um dicionário com o id do produto,
        # a quantidade e o preço, como valor. Fazendo isso, podemos garantir que um produto não é adicionado mais de
        # uma vez no carrinho.
        #
        # print(carrinho)  # {1: {'id': 1, 'quantidade': 10, 'preco': '100'}}

    def __len__(self):
        """ Conta todos os itens no carrinho. """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_lista_de_produtos(self):
        # O carrinho tem o formato abaixo:

        #   {'1': {'id': 1, 'preco': 100, 'quantidade': 5},
        #    '2': {'id': 2, 'preco': 200, 'quantidade': 3}}

        lista = []
        for item in self.carrinho.values():
            produto = Produto.objects.get(id=item['id'])
            lista.append({'produto': produto,
                          'preco': item['preco'],
                          'quantidade': item['quantidade']})

        print("<<<>>> lista = ", lista)
        return lista
        # A lista retornada tem o formato abaixo:

        # [{'produto': obj_produto1, 'preco': 100.0, 'quantidade': 5},
        #  {'produto': obj_produto2, 'preco': 200.0, 'quantidade': 3}]

    def get_lista_de_carrinhos(self):
        return self.carrinho.values()

    def adicionar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """
        print("Passou 4")

        #   {'1': {'id': 1, 'preco': 100, 'quantidade': 5},
        #    '2': {'id': 2, 'preco': 200, 'quantidade': 3}}

        produto = Produto.objects.get(id=id)
        produto_id = str(id)

        if produto_id not in self.carrinho:
            print("Passou 5")
            self.carrinho[produto_id] = {'id': produto_id, 'preco': str(produto.preco), 'quantidade': quantidade}
        else:
            # Como o objeto sessão não é modificado, isto é, apenas o objeto carrinho foi alterado,
            # logo esta modificação não será salva!
            self.carrinho[produto_id]['quantidade'] += quantidade
            if( self.carrinho[produto_id]['quantidade'] <=0):
                self.remover(id)

        print("Passou 6")
        self.salvar()        # O método salvar é chamado para que o carrinho seja salvo na sessão
        print("Passou 7")


    def alterar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """
        print("Passou 1")
        produto_id = str(id)
        print("Passou 2")

        if produto_id in self.carrinho:
            self.carrinho[produto_id]['quantidade'] = quantidade
            self.salvar()  # O método salvar é chamado para que o carrinho
                           # seja salvo na sessão.
        else:
            print("Passou 3")
            self.adicionar(id, quantidade)

        print("Passou 8")


    def remover(self, id):
        """ Remove a produto from the carrinho. """
        print("remover id = ", id)
        produto_id = str(id)

        print("remover self.carrinho = ", self.carrinho)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
            self.salvar()   # O método salvar é chamado para que o carrinho seja salvo na sessão
        print("remover self.carrinho = ", self.carrinho)

    # Nós utilizamos o id do produto como chave no carrinho. Convertemos o ID do produto em um
    # string uma vez que o Django utiliza JSON para serializar dados da sessão e o JSON apenas
    # permite strings. O ID do produto é a chave e o valor que persistimos é um dicionário com
    # o id do produto, a quantidade e o preço do produto. O preço do produto é convertido   de
    # decimal em string para ser serializado. Finalmente, chamamos o método salvar para salvar
    # o carrinho na sessão. O método  salvar salva na sessão todas as  mudanças  efetuadas  no
    # carrinho e marca a sessão como modificada utilizando session.modified = true.  Isto  diz
    # ao Django que a sessão foi modificada e que necessita ser salva.

    def salvar(self):
        # atualiza o carrinho na sessão
        self.session[settings.CARRINHO_SESSION_ID] = self.carrinho

        # Marca a sessão como "modificada" para ter certeza que ela será salva.
        # Isso não é necessário uma vez que a sessão foi alterada na linha acima.
        # self.session.modified = True

    def limpar(self):
        # Esvazia o carrinho
        self.session[settings.CARRINHO_SESSION_ID] = {}
        # self.session.modified = True

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def VerificaExistencia(self,id):
        produto_id = str(id)
        if produto_id in self.carrinho:
            return True
        else:
            return False
    def RetornaCotas(self,id):

        produto_id = str(id)

        if produto_id not in self.carrinho:
            return 0
        else:
            return self.carrinho[produto_id]['quantidade']