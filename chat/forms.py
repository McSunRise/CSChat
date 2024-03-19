from django import forms
from .models import User


class RegForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)

    class Meta:
        model = User
        fields = ['username', 'email']

    def pass_check(self):
        user_password1 = self.cleaned_data['password1']
        user_password2 = self.cleaned_data['password2']

        return user_password1 == user_password2


class LogForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
