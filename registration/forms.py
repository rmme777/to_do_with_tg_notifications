from django import forms
from .models import Users
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']

    password = forms.CharField(widget=forms.PasswordInput)


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