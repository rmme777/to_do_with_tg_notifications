from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Users
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    login = forms.EmailField(label="Введите почту")
    password1 = forms.CharField(
        label="Введите пароль", widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = Users
        fields = ("login",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'username' in self.fields:
            del self.fields['username']

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('login'),
            Field('password1'),
            Field('password2'),
            Submit('submit', 'Зарегистрироваться', css_class='btn btn-success'),
        )



class AuntieficationForm(forms.Form):
    login = forms.EmailField(label="Введите почту")
    password = forms.CharField(label="Введите пароль", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.user = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('login'),
            Field('password'),
            Submit('submit', 'Войти', css_class='btn btn-primary',)
        )

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if login and password:
            user = authenticate(username=login, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user