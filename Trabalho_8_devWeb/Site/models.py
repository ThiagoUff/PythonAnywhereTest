from django.conf import settings
from django.db import models

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, db_index=True)
    caminho = models.CharField(max_length=200, db_index=True)

    class Meta:
        db_table = 'images'
        ordering = ('id',)

    def __str__(self):
        return self.nome

class User(models.Model):
    nome = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    cpf = models.CharField(max_length=20)
    endereco = models.CharField(max_length=20)
    data_cadastro = models.DateField(null=True)


    class Meta:
        db_table = 'User'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def data_cadastro_masc(self):
        return self.data_cadastro.strftime("%d/%m/%Y")



class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=120)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    disponivel = models.BooleanField(default=True)
    data_de_cadastro = models.DateField(null=True)

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return self.nome

    def data_cadastro_masc(self):
        return self.data_de_cadastro.strftime("%d/%m/%Y")
