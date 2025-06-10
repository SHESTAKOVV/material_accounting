from django import forms
from main.models import Material


class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "article", "unit"]