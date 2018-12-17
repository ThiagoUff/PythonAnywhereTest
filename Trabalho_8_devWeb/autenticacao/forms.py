from django.contrib.auth.forms import AuthenticationForm
from django.forms import PasswordInput
from django import forms

class AuthenticationFormCustomizado(AuthenticationForm):

    error_messages = {
        'invalid_login': "Login inválido.",
        'inactive': "Conta inativa.",
    }
    username = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '30'}),
        required=True)

    password = forms.CharField(
        min_length=5,
        error_messages={'required': 'Campo obrigatório.', },
        widget=PasswordInput(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    # <input type="password"
    #        name="password"
    #        id="id_password"
    #        class="form-control form-control-sm"
    #        min-length="5"
    #        required>
