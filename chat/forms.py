from django.forms import TextInput, ModelForm, CharField, PasswordInput, Form, EmailInput
from .models import User, Message


class RegForm(ModelForm):

    password1 = CharField(
        widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password1'}),
        min_length=8,
        max_length=32
    )
    password2 = CharField(
        widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password2'}),
        min_length=8,
        max_length=32
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
        }

    def pass_check(self):
        user_password1 = self.cleaned_data['password1']
        user_password2 = self.cleaned_data['password2']

        return user_password1 == user_password2


class LogForm(Form):

    username = CharField(
        widget=TextInput(attrs={'class': 'form-input'}),
    )
    password = CharField(
        widget=PasswordInput(attrs={'class': 'form-input'}),
    )


class PassRestoreForm(Form):

    username = CharField(
        widget=TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    new_password = CharField(
        widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New password'})
    )


class FeedbackForm(Form):

    email = CharField(
        widget=EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail для обратной связи'})
    )

    feedback = CharField(
        widget=TextInput(attrs={'class': 'form-input'})
    )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
