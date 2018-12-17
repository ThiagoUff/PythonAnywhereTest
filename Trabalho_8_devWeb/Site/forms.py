from decimal import Decimal
from django import forms
from django.core.validators import RegexValidator
from Trabalho_5_devWeb import settings
from Site.models import Produto, Categoria
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id','nome', 'email', 'cpf', 'endereco', 'data_cadastro')
        # <input type="hidden" name="User_id" id="id_User_id" value="xxx">

    id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=False)

    # <input type="hidden" name="User_id" id="id_User_id" value="xxx">


    nome = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    # <input type="text"
    #        name="nome"
    #        id="id_nome"
    #        class="form-control form-control-sm"
    #        maxlength="120"
    #        required>

    email = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),

        required=True)

    # <input type="text"
    #        name="email"
    #        id="id_email"
    #        class="form-control form-control-sm"
    #        maxlength="120"
    #        required>

    cpf = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),

        required=True)

    # <input type="text"
    #        name="cpf"
    #        id="id_cpf"
    #        class="form-control form-control-sm"
    #        maxlength="120"
    #        required>

    endereco = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),

        required=True)

    # <input type="text"
    #        name="endereco"
    #        id="id_endereco"
    #        class="form-control form-control-sm"
    #        maxlength="120"
    #        required>

    # <input type="text"
    #        name="preco"
    #        id="id_preco"
    #        class="form-control form-control-sm"
    #        min_length="4"
    #        maxlength="10"
    #        onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44')
    #        required>

    data_cadastro = forms.DateField(
        input_formats = settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    # <input type="text"
    #        name="data_cadastro"
    #        class="form-control form-control-sm hasDatepicker"
    #        required=""
    #        id="id_data_cadastro"
    #        maxlength="10">

class RemoveUserForm(forms.Form):
    class Meta:
        fields = ('id')

    id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=False)
    # <input type="hidden" name="User_id" id="id_User_id" value="xxx">

class AtualizaProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        # O campo fields abaixo impede que seja atualizado um campo não especificado na lista abaixo. Deve ser especificado o
        # campo fields ou o campo exclude.
        fields = ('produto_id', 'estoque')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    estoque = forms.IntegerField(
        min_value=1,
        max_value=1000,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm estoque',
                                      'maxlength': '20',
                                      'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'}),
        required=True)

class PesquisaProdutoForm(forms.Form):
    class Meta:
        fields = ('buscaPor')

    buscaPor = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False)

class ProdutoForm(forms.ModelForm):

    error_messages = {
        'campo_invalido': "Valor de estoque inválido.",
        'estoque_invalido': "O estoque deve ser > zero.",
    }

    class Meta:
        model = Produto
        # O campo fields abaixo impede que seja atualizado um campo não especificado na lista abaixo. Deve ser especificado o
        # campo fields ou o campo exclude.
        fields = ('produto_id', 'categoria', 'nome', 'preco', 'estoque', 'disponivel', 'data_de_cadastro')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    categoria = forms.ModelChoiceField(
        error_messages={'required': 'Campo obrigatório.', },
        queryset=Categoria.objects.all().order_by('nome'),
        empty_label='--- Selecione a Categoria ---',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    nome = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    preco = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        min_length=4, validators=[
            RegexValidator(regex='^[0-9]{1,7}(,[0-9]{2})?$', message="Informe o preço no formato 9999999,99.")],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'maxlength': '10',
                                      'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'}),
        required=True)

    estoque = forms.IntegerField(
        min_value=0,
        max_value=1000,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'maxlength': '20',
                                      'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'}),
        required=True)

    data_de_cadastro = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    # disponivel = forms.BooleanField(
    #     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    #     required=False)

    disponivel = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        required=False)

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')

        preco = Decimal(preco.replace(',', '.'))

        return preco

    def clean_estoque(self):
        estoque = self.cleaned_data.get('estoque')

        if not estoque:
            return estoque

        if estoque > 900:
            raise forms.ValidationError(
                self.error_messages['campo_invalido'], code='campo_invalido',
            )
        return estoque

    def clean(self):
        estoque = self.cleaned_data.get('estoque')
        disponivel = self.cleaned_data.get('disponivel')

        if disponivel and estoque == 0:
            self.add_error('estoque', "Como o produto está disponível, o estoque deve ser > zero.")
            # raise forms.ValidationError(self.error_messages['estoque_invalido'], code='estoque_invalido'})

        return self.cleaned_data

class RemoveProdutoForm(forms.Form):
    class Meta:
        fields = ('produto_id' )

    produto_id = forms.CharField(widget=forms.HiddenInput())

class ColocaProdutoCarrinhoForm(forms.Form):
    class Meta:
        fields = ('produto_id','produto_qtd')

    produto_id = forms.CharField(widget=forms.HiddenInput())
    produto_qtd = forms.IntegerField(widget=forms.HiddenInput())

